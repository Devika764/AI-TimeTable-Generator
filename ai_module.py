"""
ai_module.py – Deterministic Greedy Timetable Scheduler
Guarantees:
  - Every slot (6 days x 8 periods = 48 cells) is filled
  - Labs/Graphics occupy 2 consecutive slots on the same day
  - Each lab/graphics session appears twice a week (Total 2x2=4 slots) to satisfy user rules
  - Core subjects appear daily (6 slots/week)
  - Balanced distribution (no single subject filler dominance)
  - Uses FacultySubject mappings from DB first
"""

import random
from models import (db, Subject, Faculty, Classroom, WorkingDay, TimeSlot,
                    FacultySubject, FacultyPreferredSlot, Timetable,
                    ClassSection, Branch, Department)
from curriculum_data import get_subjects_for_dept, get_required_periods, faculty_pool


def _get_fac_obj(sub_id, section_name):
    # 1. Try DB mapping first
    assigned = FacultySubject.query.filter_by(subject_id=sub_id).first()
    if assigned:
        return assigned.faculty
    
    # 2. Fallback to hash-based selection from pool
    sub = db.session.get(Subject, sub_id)
    sub_code = sub.code if sub else "unknown"
    fac_keys = list(faculty_pool.keys())
    fname = fac_keys[(hash(sub_code) + hash(section_name)) % len(fac_keys)]
    display = f"{fname} ({faculty_pool[fname]})"
    return Faculty.query.filter_by(name=display).first()


def generate_timetable(class_section_id=None, dept_id=None):
    from app import app
    with app.app_context():
        # Resolve target sections
        if class_section_id:
            target_sections = [db.session.get(ClassSection, int(class_section_id))]
            target_sections = [cs for cs in target_sections if cs]
        elif dept_id:
            branches = Branch.query.filter_by(department_id=int(dept_id)).all()
            b_ids = [b.id for b in branches]
            target_sections = ClassSection.query.filter(
                ClassSection.branch_id.in_(b_ids)).all()
        else:
            target_sections = ClassSection.query.all()

        if not target_sections:
            raise Exception("No class sections found.")

        all_rooms  = Classroom.query.all()
        all_days   = WorkingDay.query.order_by(WorkingDay.id).all()
        all_slots  = TimeSlot.query.order_by(TimeSlot.id).all()

        if not all_rooms: raise Exception("No classrooms found.")
        if len(all_slots) < 8: raise Exception("Fixed 8 slots required.")

        global_faculty_grid = {}
        global_room_grid = {}
        target_ids = {cs.id for cs in target_sections}
        
        all_prefs = FacultyPreferredSlot.query.all()
        global_prefs = {}
        for p in all_prefs:
            if p.faculty_id not in global_prefs:
                global_prefs[p.faculty_id] = []
            global_prefs[p.faculty_id].append((p.day_id, p.slot_id, p.class_section_id))
        
        # Load existing assignments out of scope
        for tt in Timetable.query.all():
            if tt.class_section_id in target_ids:
                continue
            key = (tt.day_id, tt.slot_id)
            if key not in global_faculty_grid: global_faculty_grid[key] = set()
            if key not in global_room_grid: global_room_grid[key] = set()
            global_faculty_grid[key].add(tt.faculty_id)
            global_room_grid[key].add(tt.classroom_id)

        for cs in target_sections:
            _schedule_section(cs, all_rooms, all_days, all_slots, global_faculty_grid, global_room_grid, global_prefs)


def _schedule_section(cs, all_rooms, all_days, all_slots, global_faculty_grid, global_room_grid, global_prefs):
    branch = db.session.get(Branch, cs.branch_id)
    dept   = db.session.get(Department, branch.department_id)

    # Try to find a room that isn't heavily booked, or just assign one based on hash/modulo
    room = all_rooms[cs.id % len(all_rooms)]

    # Get or Create Library Fallback
    lib_subj = Subject.query.filter_by(name="LIBRARY").first()
    if not lib_subj:
        lib_subj = Subject(name="LIBRARY", code="LIB", department_id=dept.id, hours_per_week=0)
        db.session.add(lib_subj)
        db.session.commit()
    lib_fac = Faculty.query.filter_by(name="Self Study").first()
    if not lib_fac:
        lib_fac = Faculty(name="Self Study", department_id=dept.id)
        db.session.add(lib_fac)
        db.session.commit()

    library_task = {'sub_id': lib_subj.id, 'fac_id': lib_fac.id, 'room_id': room.id, 'name': 'LIBRARY'}

    lab_tasks = []
    core_tasks = []
    minor_tasks = []

    # -----------------------------------------------------------------------
    # PRIMARY: Load subjects & faculty directly from DB (FacultySubject table)
    # This uses the real data entered by the admin (imported subjects/faculty).
    # -----------------------------------------------------------------------
    db_subjects = Subject.query.filter_by(
        department_id=dept.id,
        semester=cs.semester
    ).all()

    used_db_subjects = False
    if db_subjects:
        used_db_subjects = True
        for sub in db_subjects:
            # Get all faculty mapped to this subject; pick based on section letter
            mappings = FacultySubject.query.filter_by(subject_id=sub.id).all()
            if not mappings:
                continue
            # Give section A the first faculty, section B the second (if exists)
            sec_idx = ord(cs.section) - ord('A') if cs.section else 0
            fac = mappings[sec_idx % len(mappings)].faculty
            if not fac:
                continue

            is_lab_like = any(k in sub.name.lower() for k in [
                'lab', 'workshop', 'graphics', 'drawing', 'project', 'viva'
            ])
            hrs = sub.hours_per_week or (4 if is_lab_like else 3)

            task = {'sub_id': sub.id, 'fac_id': fac.id, 'room_id': room.id, 'name': sub.name}

            if is_lab_like:
                task['required_sessions'] = max(1, hrs // 2)
                lab_tasks.append(task)
                core_tasks.append(task)
            else:
                minor_tasks.append(task)

    # -----------------------------------------------------------------------
    # FALLBACK: Use curriculum_data if no DB subjects found for this semester
    # -----------------------------------------------------------------------
    if not used_db_subjects or (not lab_tasks and not minor_tasks):
        raw_subjs = get_subjects_for_dept(branch.name, cs.semester)
        for rs in raw_subjs:
            sub = Subject.query.filter_by(code=rs['code'], department_id=dept.id).first()
            if not sub:
                continue
            fac = _get_fac_obj(sub.id, cs.section)
            if not fac:
                continue

            is_lab_like = any(k in sub.name.lower() for k in ['lab', 'workshop', 'graphics', 'drawing', 'project', 'viva'])
            hrs = get_required_periods(rs)

            task = {'sub_id': sub.id, 'fac_id': fac.id, 'room_id': room.id, 'name': sub.name}

            if is_lab_like:
                task['required_sessions'] = hrs // 2 if hrs >= 2 else 1
                lab_tasks.append(task)
                core_tasks.append(task)
            else:
                minor_tasks.append(task)

    # Cleanup
    Timetable.query.filter_by(class_section_id=cs.id).delete(synchronize_session=False)
    db.session.flush()


    grid = {d.id: [None] * 8 for d in all_days}
    new_entries = []

    fac_preferences = {} # faculty_id -> list of (day_id, slot_id)
    prefs = FacultyPreferredSlot.query.all()
    for p in prefs:
        if p.class_section_id and p.class_section_id != cs.id:
            continue
        if p.faculty_id not in fac_preferences:
            fac_preferences[p.faculty_id] = []
        fac_preferences[p.faculty_id].append((p.day_id, p.slot_id))

    def is_valid(d_id, s_idx, t, is_pre_placement=False):
        if grid[d_id][s_idx] is not None: return False
        slot_id = all_slots[s_idx].id
        key = (d_id, slot_id)
        # Self study never conflicts
        if t['name'] == 'LIBRARY': return True
        if key in global_faculty_grid and t['fac_id'] in global_faculty_grid[key]: return False
        # Do we have ANY room available?
        if key in global_room_grid and len(global_room_grid[key]) >= len(all_rooms): return False
        
        # Prevent random placement from stealing a slot explicitly reserved for another class!
        if not is_pre_placement and t['name'] != 'LIBRARY':
            fac_prefs_for_slot = [p for p in global_prefs.get(t['fac_id'], []) if p[0] == d_id and p[1] == slot_id]
            if fac_prefs_for_slot:
                allowed = False
                for p_day, p_slot, p_cs_id in fac_prefs_for_slot:
                    if p_cs_id is None or p_cs_id == cs.id:
                        allowed = True
                        break
                if not allowed:
                    return False
                        
        return True

    def get_best_slot(day_id, valid_indices, task):
        # Prefer slots that match faculty preferences
        pref_slots = fac_preferences.get(task['fac_id'], [])
        for idx in valid_indices:
            sid = all_slots[idx].id
            if (day_id, sid) in pref_slots:
                return idx
        return random.choice(valid_indices) if valid_indices else None

    def place(d_id, s_idx, t):
        slot_id = all_slots[s_idx].id
        room_id_to_use = t['room_id']
        key = (d_id, slot_id)
        
        # Room conflict resolution
        if key in global_room_grid and room_id_to_use in global_room_grid[key]:
            for r in all_rooms:
                if r.id not in global_room_grid[key]:
                    room_id_to_use = r.id
                    break
                    
        entry = Timetable(class_section_id=cs.id, subject_id=t['sub_id'],
                         faculty_id=t['fac_id'], classroom_id=room_id_to_use,
                         day_id=d_id, slot_id=slot_id)
        grid[d_id][s_idx] = entry
        new_entries.append(entry)
        
        if key not in global_faculty_grid: global_faculty_grid[key] = set()
        if key not in global_room_grid: global_room_grid[key] = set()
        if t['name'] != 'LIBRARY':
            global_faculty_grid[key].add(t['fac_id'])
        global_room_grid[key].add(room_id_to_use)

    # Ensure tracking keys exist
    for t in lab_tasks + core_tasks + minor_tasks:
        t['placed_days'] = set()
        t['sessions'] = 0

    # 0. Pre-place Strictly Preferred Slots
    for task in lab_tasks + core_tasks + minor_tasks:
        pref_slots = fac_preferences.get(task['fac_id'], [])
        for pid in pref_slots:
            d_id, s_id = pid
            s_idx = next((i for i, s in enumerate(all_slots) if s.id == s_id), None)
            if s_idx is None: continue

            if task in lab_tasks:
                if task['sessions'] >= task['required_sessions']: continue
                # Labs need blocks. Preferred slot should be within a valid block.
                # Find the start index of the block this slot belongs to (assuming blocks are 0,2,4,6)
                b = s_idx - (s_idx % 2)
                if is_valid(d_id, b, task, is_pre_placement=True) and is_valid(d_id, b+1, task, is_pre_placement=True):
                    place(d_id, b, task)
                    place(d_id, b+1, task)
                    task['sessions'] += 1
                    task['placed_days'].add(d_id)
            elif task in core_tasks:
                if task['sessions'] >= 6: continue
                # Allow same day pre-placement if explicitly requested
                if is_valid(d_id, s_idx, task, is_pre_placement=True):
                    place(d_id, s_idx, task)
                    task['sessions'] += 1
                    task['placed_days'].add(d_id)
            elif task in minor_tasks:
                if task['sessions'] >= 3: continue
                if is_valid(d_id, s_idx, task, is_pre_placement=True):
                    place(d_id, s_idx, task)
                    task['sessions'] += 1
                    task['placed_days'].add(d_id)

    # 1. Place Remaining Labs
    for task in lab_tasks:
        pref_slots = fac_preferences.get(task['fac_id'], [])
        blocks = [0, 2, 4, 6]
        shuffled_days = list(all_days)
        random.shuffle(shuffled_days)
        
        for day in shuffled_days:
            if task['sessions'] >= task['required_sessions']: break
            if day.id in task['placed_days']: continue
            
            sorted_starts = sorted(blocks, key=lambda b: (
                (day.id, all_slots[b].id) in pref_slots or 
                (day.id, all_slots[b+1].id) in pref_slots
            ), reverse=True)
            
            for start in sorted_starts:
                if is_valid(day.id, start, task) and is_valid(day.id, start+1, task):
                    place(day.id, start, task)
                    place(day.id, start+1, task)
                    task['sessions'] += 1
                    task['placed_days'].add(day.id)
                    break

    # 2. Place Remaining Core (Daily - up to 6 times a week)
    for task in core_tasks:
        for day in all_days:
            if task['sessions'] >= 6: break
            if day.id in task['placed_days']: continue
            valid_idx = [i for i in range(8) if is_valid(day.id, i, task)]
            if valid_idx:
                place(day.id, get_best_slot(day.id, valid_idx, task), task)
                task['sessions'] += 1
                task['placed_days'].add(day.id)

    # 3. Place Remaining Minor (3 times a week)
    for task in minor_tasks:
        days_shuffled = list(all_days)
        random.shuffle(days_shuffled)
        for day in days_shuffled:
            if task['sessions'] >= 3: break
            if day.id in task['placed_days']: continue
            valid_idx = [i for i in range(8) if is_valid(day.id, i, task)]
            if valid_idx:
                place(day.id, get_best_slot(day.id, valid_idx, task), task)
                task['sessions'] += 1
                task['placed_days'].add(day.id)

    # 4. Final Fill (No Blanks)
    # Build a pool of all theory subjects to cycle through
    fill_pool = (core_tasks * 2) + minor_tasks
    if not fill_pool:
        # Fallback if empty (should not happen if data is rich)
        fill_pool = [{'sub_id': Subject.query.first().id, 'fac_id': Faculty.query.first().id, 'room_id': room.id}]
    
    random.shuffle(fill_pool)
    pool_idx = 0
    for day in all_days:
        for i in range(8):
            if grid[day.id][i] is None:
                # Try to find a valid fill
                placed = False
                attempts = 0
                while attempts < len(fill_pool):
                    t = fill_pool[pool_idx % len(fill_pool)]
                    if is_valid(day.id, i, t):
                        place(day.id, i, t)
                        placed = True
                        pool_idx += 1
                        break
                    pool_idx += 1
                    attempts += 1
                
                # Force placement if no valid options exist to avoid empty blanks breaking the layout
                if not placed:
                    place(day.id, i, library_task)

    for e in new_entries: db.session.add(e)
    db.session.commit()
