"""
seed_curriculum.py
──────────────────
Reads from curriculum_data.py and populates the database with:
  • Departments  (AI, CSE, IT, ECE, EEE)
  • Faculty      (assigned to the right department)
  • Subjects     (per-department, de-duplicated)
  • FacultySubject mappings
  • Classrooms   (1201-1299)
  • WorkingDays / TimeSlots
  • Branch + ClassSection hierarchy  (kept in sync with app.py startup seed)

Run once from the project root:
    python seed_curriculum.py
"""

import os, sys, random
from app import app, db
from models import (Admin, Department, Branch, ClassSection,
                    Subject, Faculty, FacultySubject,
                    Classroom, WorkingDay, TimeSlot)
from curriculum_data import (faculty_pool, get_subjects_for_dept,
                              get_required_periods, room_numbers)

# ──────────────────────────────────────────────────────────────────────────────
# Structure: (dept_name, branch_name, sections)
# ──────────────────────────────────────────────────────────────────────────────
STRUCTURE = [
    ('AI',  'AIML', ['A', 'B']),
    ('AI',  'AIDS', ['A', 'B']),
    ('CSE', 'CSE',  ['A', 'B']),
    ('IT',  'IT',   ['A', 'B']),
    ('ECE', 'ECE',  ['A', 'B']),
    ('EEE', 'EEE',  ['A', 'B']),
    ('MECH', 'MECH', ['A', 'B']),
    ('CIVIL', 'CIVIL', ['A', 'B']),
]

# Map each branch → the parent department name
BRANCH_TO_DEPT = {branch: dept for dept, branch, _ in STRUCTURE}

# ──────────────────────────────────────────────────────────────────────────────
# Faculty distribution: which departments each faculty pool member covers.
# We split the faculty pool alphabetically across departments.
# ──────────────────────────────────────────────────────────────────────────────
DEPT_NAMES = ['AI', 'CSE', 'IT', 'ECE', 'EEE', 'MECH', 'CIVIL']
faculty_names = list(faculty_pool.keys())
FACULTY_DEPT_MAP = {}   # faculty_name → dept_name
for idx, fname in enumerate(faculty_names):
    FACULTY_DEPT_MAP[fname] = DEPT_NAMES[idx % len(DEPT_NAMES)]

# ──────────────────────────────────────────────────────────────────────────────
with app.app_context():
    print("\n[START] Starting full database seed from curriculum_data.py ...\n")

    # ------------------------------------------------------------------
    # 1.  Drop & recreate all tables cleanly
    # ------------------------------------------------------------------
    print("  [1/8] Dropping old tables...")
    db.drop_all()
    print("  [1/8] Creating fresh tables...")
    db.create_all()

    # ------------------------------------------------------------------
    # 2.  Default admin
    # ------------------------------------------------------------------
    print("  [2/8] Creating admin user...")
    admin = Admin(username='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()

    # ------------------------------------------------------------------
    # 3.  Working days
    # ------------------------------------------------------------------
    print("  [3/8] Adding working days...")
    for d_name in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
        db.session.add(WorkingDay(day_name=d_name))
    db.session.commit()

    # ------------------------------------------------------------------
    # 4.  Time slots  (8 periods per day)
    # ------------------------------------------------------------------
    print("  [4/8] Adding time slots...")
    time_slots = [
        ("09:00", "09:50"), ("09:50", "10:40"), ("10:40", "11:30"), ("11:30", "12:20"),
        ("13:10", "14:00"), ("14:00", "14:50"), ("14:50", "15:40"), ("15:40", "16:30"),
    ]
    for s, e in time_slots:
        db.session.add(TimeSlot(start_time=s, end_time=e))
    db.session.commit()

    # ------------------------------------------------------------------
    # 5.  Classrooms  (1201 – 1299)
    # ------------------------------------------------------------------
    print("  [5/8] Adding classrooms (1201-1299)...")
    for room_no in room_numbers:
        db.session.add(Classroom(name=str(room_no), capacity=60))
    db.session.commit()

    # ------------------------------------------------------------------
    # 6.  Departments + Branches + ClassSections
    # ------------------------------------------------------------------
    print("  [6/8] Creating Departments / Branches / Sections...")
    dept_db   = {}   # dept_name  → Department ORM obj
    branch_db = {}   # branch_name → Branch ORM obj

    # Create departments first
    for dept_name in DEPT_NAMES:
        dept_obj = Department(name=dept_name)
        db.session.add(dept_obj)
        db.session.flush()
        dept_db[dept_name] = dept_obj

    # Create branches + sections
    for dept_name, branch_name, sections in STRUCTURE:
        dept_obj = dept_db[dept_name]
        branch_obj = Branch(name=branch_name, department_id=dept_obj.id)
        db.session.add(branch_obj)
        db.session.flush()
        branch_db[branch_name] = branch_obj

        for sem in range(1, 9):
            for sec in sections:
                db.session.add(ClassSection(
                    branch_id=branch_obj.id,
                    semester=sem,
                    section=sec
                ))

    db.session.commit()
    print(f"     -> {len(dept_db)} departments | {len(branch_db)} branches created")

    # ------------------------------------------------------------------
    # 7.  Faculty  (assigned to departments)
    # ------------------------------------------------------------------
    print("  [7/8] Adding faculty members...")
    faculty_db_map = {}   # faculty_name → Faculty ORM obj

    for fac_name, fac_code in faculty_pool.items():
        dept_name = FACULTY_DEPT_MAP[fac_name]
        dept_obj  = dept_db[dept_name]
        display   = f"{fac_name} ({fac_code})"
        fac_obj   = Faculty(name=display, department_id=dept_obj.id)
        db.session.add(fac_obj)
        db.session.flush()
        faculty_db_map[fac_name] = fac_obj   # keyed by plain name

    db.session.commit()
    print(f"     -> {len(faculty_db_map)} faculty members added")

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # 8.  Subjects  (per-department, de-duplicated by code per dept)
    #     + FacultySubject assignments
    # ------------------------------------------------------------------
    print("  [8/8] Populating subjects & faculty assignments with STRICT LOAD BALANCING...")

    subject_count = 0
    fs_count = 0
    subject_db_map = {}

    # Track faculty workloads: {faculty_id: {'theory': 0, 'lab': 0}}
    faculty_loads = {f.id: {'theory': 0, 'lab': 0} for f in faculty_db_map.values()}

    for dept_name, branch_name, sections in STRUCTURE:
        dept_obj = dept_db[dept_name]
        
        # Get all faculty belonging to this department
        dept_faculties = [f for key, f in faculty_db_map.items() if f.department_id == dept_obj.id]

        for sem in range(1, 9):
            raw_subjects = get_subjects_for_dept(branch_name, sem)

            for subj in raw_subjects:
                code = subj['code']
                key  = (dept_name, code)
                is_lab = subj.get('lab', False) or any(k in subj['name'].lower() for k in ['lab', 'workshop', 'project', 'viva'])

                # De-duplicate: add subject to DB only once per dept
                if key not in subject_db_map:
                    hrs = get_required_periods(subj)
                    sub_obj = Subject(
                        code=code,
                        name=subj['name'],
                        department_id=dept_obj.id,
                        hours_per_week=hrs
                    )
                    db.session.add(sub_obj)
                    db.session.flush()
                    subject_db_map[key] = sub_obj
                    subject_count += 1

                sub_obj = subject_db_map[key]

                # Assign DIFFERENT faculty for each section for the same subject
                for sec in sections:
                    assigned_fac = None
                    
                    random.shuffle(dept_faculties) # shuffle to balance
                    
                    for fac in dept_faculties:
                        load = faculty_loads[fac.id]
                        if is_lab:
                            if load['lab'] < 3:
                                assigned_fac = fac
                                load['lab'] += 1
                                break
                        else:
                            if load['theory'] < 3:
                                assigned_fac = fac
                                load['theory'] += 1
                                break
                                
                    if not assigned_fac:
                        # Fallback if somehow department faculty is exhausted: use ANY low-load faculty globally
                        all_fac_list = list(faculty_db_map.values())
                        random.shuffle(all_fac_list)
                        for fac in all_fac_list:
                            load = faculty_loads[fac.id]
                            if is_lab and load['lab'] < 3:
                                assigned_fac = fac
                                load['lab'] += 1
                                break
                            elif not is_lab and load['theory'] < 3:
                                assigned_fac = fac
                                load['theory'] += 1
                                break
                    
                    if not assigned_fac:
                        # Absolute emergency fallback, shouldn't happen with 350 faculty
                        assigned_fac = dept_faculties[0]
                        print("WARNING: Faculty over-allocated!")

                    # Avoid duplicate FacultySubject rows (a faculty might be assigned to both sections hypothetically, but we want distinct mapping)
                    exists = FacultySubject.query.filter_by(faculty_id=assigned_fac.id, subject_id=sub_obj.id).first()
                    if not exists:
                        db.session.add(FacultySubject(faculty_id=assigned_fac.id, subject_id=sub_obj.id))
                        fs_count += 1
    db.session.commit()
    print(f"     -> {subject_count} subjects added")
    print(f"     -> {fs_count} faculty-subject mappings created")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n[DONE] Seeding complete!\n")
    print("-" * 50)
    print(f"  Departments  : {Department.query.count()}")
    print(f"  Branches     : {Branch.query.count()}")
    print(f"  ClassSections: {ClassSection.query.count()}")
    print(f"  Subjects     : {Subject.query.count()}")
    print(f"  Faculty      : {Faculty.query.count()}")
    print(f"  Classrooms   : {Classroom.query.count()}")
    print(f"  Working Days : {WorkingDay.query.count()}")
    print(f"  Time Slots   : {TimeSlot.query.count()}")
    print(f"  FA Mappings  : {FacultySubject.query.count()}")
    print("-" * 50)
    print("\n  Login: admin / admin123")
    print("  Run:   python app.py\n")
