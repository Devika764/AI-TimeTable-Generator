from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, date
import os

from models import (db, Admin, Course, Department, Branch, ClassSection, Subject, Faculty, 
                    Classroom, WorkingDay, TimeSlot, FacultySubject, FacultyPreferredSlot, Timetable)
from ai_module import generate_timetable
from curriculum_data import get_abbreviation, get_subjects_for_dept, faculty_pool
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timetable.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Admin, int(user_id))

# --- ROUTES ---

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_course':
            course_name = request.form.get('course_name')
            if course_name:
                existing_course = Course.query.filter_by(name=course_name).first()
                if existing_course:
                    flash(f"Course '{course_name}' already exists!", 'warning')
                else:
                    new_course = Course(name=course_name)
                    db.session.add(new_course)
                    try:
                        db.session.commit()
                        flash('Course added!', 'success')
                    except Exception as e:
                        db.session.rollback()
                        flash(f"Error adding course: {str(e)}", 'danger')
        return redirect(url_for('dashboard'))

    stats = {
        'courses': Course.query.count(),
        'departments': Department.query.count(),
        'faculty': Faculty.query.count(),
        'subjects': Subject.query.count(),
        'sections': ClassSection.query.count(),
        'timetables': Timetable.query.distinct(Timetable.class_section_id).count()
    }
    depts = Department.query.all()
    courses = Course.query.all()
    return render_template('dashboard.html', stats=stats, departments=depts, courses=courses)

# --- CRUD ROUTES ---

@app.route('/departments', methods=['GET', 'POST'])
@login_required
def departments():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            existing_dept = Department.query.filter_by(name=name).first()
            if existing_dept:
                flash(f"Department '{name}' already exists!", 'warning')
            else:
                new_dept = Department(name=name)
                db.session.add(new_dept)
                try:
                    db.session.commit()
                    flash('Department added!', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash(f"Error adding department: {str(e)}", 'danger')
    depts = Department.query.all()
    return render_template('departments.html', depts=depts, departments=depts)

@app.route('/faculty', methods=['GET', 'POST'])
@login_required
def faculty():
    if request.method == 'POST':
        name = request.form.get('name')
        dept_id = request.form.get('department_id')
        if name and dept_id:
            new_faculty = Faculty(name=name, department_id=dept_id)
            db.session.add(new_faculty)
            db.session.commit()
            flash('Faculty added!', 'success')
    faculties = Faculty.query.all()
    depts = Department.query.all()
    return render_template('faculty.html', faculty=faculties, departments=depts)

@app.route('/subjects', methods=['GET', 'POST'])
@login_required
def subjects():
    if request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        dept_id = request.form.get('department_id')
        hours = request.form.get('hours_per_week', type=int)
        semester = request.form.get('semester', type=int)
        subject_type = request.form.get('subject_type', 'Theory')
        regulation = request.form.get('regulation', 'R20')
        
        # Determine credits
        credits_val = request.form.get('credits', type=float)
        if credits_val is None:
            credits_val = 3.0 if subject_type == 'Theory' else 1.5
            
        if name and dept_id:
            new_sub = Subject(code=code, name=name, department_id=dept_id, semester=semester, hours_per_week=hours or 4, subject_type=subject_type, credits=credits_val, regulation=regulation)
            db.session.add(new_sub)
            db.session.commit()
            flash('Subject added!', 'success')
            return redirect(url_for('subjects'))

    dept_filter = request.args.get('filter_dept')
    sem_filter = request.args.get('filter_sem')
    reg_filter = request.args.get('filter_reg')
    
    query = Subject.query
    if dept_filter:
        query = query.filter_by(department_id=dept_filter)
    if sem_filter:
        query = query.filter_by(semester=sem_filter)
    if reg_filter:
        query = query.filter_by(regulation=reg_filter)
        
    subs = query.all()
    depts = Department.query.all()
    
    regulations = db.session.query(Subject.regulation).distinct().all()
    regulations = [r[0] for r in regulations if r[0]]
    if not regulations:
        regulations = ['R16', 'R19', 'R20', 'R23']
    else:
        for r in ['R16', 'R19', 'R20', 'R23']:
            if r not in regulations:
                regulations.append(r)
        regulations.sort()

    return render_template('subjects.html', subjects=subs, departments=depts, sel_dept=dept_filter, sel_sem=sem_filter, sel_reg=reg_filter, regulations=regulations)

@app.route('/classrooms', methods=['GET', 'POST'])
@login_required
def classrooms():
    if request.method == 'POST':
        name = request.form.get('name')
        cap = request.form.get('capacity', type=int)
        if name and cap:
            new_room = Classroom(name=name, capacity=cap)
            db.session.add(new_room)
            db.session.commit()
            flash('Classroom added!', 'success')
    rooms = Classroom.query.all()
    return render_template('classrooms.html', classrooms=rooms)

@app.route('/timeslots', methods=['GET', 'POST'])
@login_required
def timeslots():
    if request.method == 'POST':
        start = request.form.get('start_time')
        end = request.form.get('end_time')
        if start and end:
            new_slot = TimeSlot(start_time=start, end_time=end)
            db.session.add(new_slot)
            db.session.commit()
            flash('Time slot added!', 'success')
    slots = TimeSlot.query.all()
    return render_template('timeslots.html', timeslots=slots)

@app.route('/mappings', methods=['GET', 'POST'])
@login_required
def mappings():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'assign_subject':
            f_id = request.form.get('faculty_id')
            s_id = request.form.get('subject_id')
            if f_id and s_id:
                new_map = FacultySubject(faculty_id=f_id, subject_id=s_id)
                db.session.add(new_map)
                db.session.commit()
                flash('Subject assigned to faculty!', 'success')
        elif action == 'assign_pref':
            f_id = request.form.get('faculty_id')
            cs_id = request.form.get('class_section_id') # Optional
            d_id = request.form.get('day_id')
            s_id = request.form.get('slot_id')
            if f_id and d_id and s_id:
                # cs_id can be empty string if "All Classes" is selected
                cs_id_val = int(cs_id) if cs_id and cs_id.strip() else None
                new_pref = FacultyPreferredSlot(
                    faculty_id=f_id, 
                    class_section_id=cs_id_val,
                    day_id=d_id, 
                    slot_id=s_id
                )
                db.session.add(new_pref)
                db.session.commit()
                flash('Faculty preference added!', 'success')
    
    faculties = Faculty.query.all()
    subjects = Subject.query.all()
    days = WorkingDay.query.all()
    slots = TimeSlot.query.all()
    fs_mappings = FacultySubject.query.all()
    pref_mappings = FacultyPreferredSlot.query.all()
    all_sections = ClassSection.query.all()
    return render_template('mappings.html', 
                          faculties=faculties, subjects=subjects, 
                          days=days, slots=slots,
                          fs_mappings=fs_mappings, pref_mappings=pref_mappings,
                          all_sections=all_sections)

# --- DELETE ROUTES ---

@app.route('/delete_course/<int:id>', methods=['POST'])
@login_required
def delete_course(id):
    obj = db.session.get(Course, id)
    if obj:
        db.session.delete(obj)
        db.session.commit()
        flash('Course deleted.', 'info')
    return redirect(url_for('dashboard'))

@app.route('/delete_department/<int:id>', methods=['POST'])
@login_required
def delete_department(id):
    obj = db.session.get(Department, id)
    if obj:
        db.session.delete(obj)
        db.session.commit()
        flash('Department deleted.', 'info')
    return redirect(url_for('departments'))

@app.route('/delete_faculty/<int:id>', methods=['POST'])
@login_required
def delete_faculty(id):
    obj = db.session.get(Faculty, id)
    if obj:
        db.session.delete(obj)
        db.session.commit()
        flash('Faculty deleted.', 'info')
    return redirect(url_for('faculty'))

@app.route('/delete_subject/<int:id>', methods=['POST'])
@login_required
def delete_subject(id):
    obj = db.session.get(Subject, id)
    if obj:
        db.session.delete(obj)
        db.session.commit()
        flash('Subject deleted.', 'info')
    return redirect(url_for('subjects'))

@app.route('/delete_classroom/<int:id>', methods=['POST'])
@login_required
def delete_classroom(id):
    obj = db.session.get(Classroom, id)
    if obj:
        db.session.delete(obj)
        db.session.commit()
        flash('Classroom deleted.', 'info')
    return redirect(url_for('classrooms'))

@app.route('/delete_timeslot/<int:id>', methods=['POST'])
@login_required
def delete_timeslot(id):
    obj = db.session.get(TimeSlot, id)
    if obj:
        db.session.delete(obj)
        db.session.commit()
        flash('Time slot deleted.', 'info')
    return redirect(url_for('timeslots'))

@app.route('/delete_fs/<int:id>', methods=['POST'])
@login_required
def delete_fs(id):
    obj = db.session.get(FacultySubject, id)
    if obj:
        db.session.delete(obj)
        db.session.commit()
        flash('Assignment removed.', 'info')
    return redirect(url_for('mappings'))

@app.route('/delete_pref/<int:id>', methods=['POST'])
@login_required
def delete_pref(id):
    obj = db.session.get(FacultyPreferredSlot, id)
    if obj:
        db.session.delete(obj)
        db.session.commit()
        flash('Preference removed.', 'info')
    return redirect(url_for('mappings'))

# --- API HELPERS ---

@app.route('/api/branches')
@login_required
def api_branches():
    dept_id = request.args.get('dept_id')
    branches = Branch.query.filter_by(department_id=dept_id).all()
    return jsonify([{'id': b.id, 'name': b.name} for b in branches])

@app.route('/api/semesters')
@login_required
def api_semesters():
    branch_id = request.args.get('branch_id')
    # For simplicity, returning 8 semesters. In a real app, this might be filtered.
    return jsonify([{'semester': i, 'label': f'Semester {i}'} for i in range(1, 9)])

@app.route('/api/sections')
@login_required
def api_sections(branch_id=None, semester=None):
    b_id = request.args.get('branch_id') or branch_id
    sem = request.args.get('semester') or semester
    sections = ClassSection.query.filter_by(branch_id=b_id, semester=sem).all()
    return jsonify([{'id': s.id, 'section': s.section} for s in sections])

@app.route('/api/dept_subjects')
def api_dept_subjects():
    dept_id = request.args.get('dept_id')
    if not dept_id:
        return jsonify([])
    subjects = Subject.query.filter_by(department_id=dept_id).all()
    return jsonify([{'id': s.id, 'name': s.name, 'code': s.code or ''} for s in subjects])

@app.route('/api/dept_faculty_subjects')
@login_required
def api_dept_faculty_subjects():
    dept_id = request.args.get('dept_id')
    sub_id = request.args.get('subject_id')
    
    if not dept_id:
        return jsonify([])
    
    # Query all subjects mapped to this department, optionally filtered by specific subject
    query = Subject.query.filter_by(department_id=dept_id)
    if sub_id:
        query = query.filter_by(id=sub_id)
        
    subjects = query.all()
    result = []
    
    for sub in subjects:
        # Get all faculty mappings for this specific subject
        mappings = FacultySubject.query.filter_by(subject_id=sub.id).all()
        # Extract faculty names
        faculty_names = [m.faculty.name for m in mappings if m.faculty]
        
        result.append({
            'code': sub.code or '---',
            'name': sub.name,
            'hours': sub.hours_per_week,
            'faculty': ', '.join(faculty_names) if faculty_names else 'Not Assigned'
        })
        
    return jsonify(result)

@app.route('/api/subjects_by_class')
def api_subjects_by_class():
    """Returns subjects + faculty actually scheduled in a specific class section (branch + semester)."""
    branch_id = request.args.get('branch_id')
    semester  = request.args.get('semester')

    if not branch_id or not semester:
        return jsonify([])

    # Find all sections matching branch + semester
    sections = ClassSection.query.filter_by(branch_id=branch_id, semester=semester).all()
    if not sections:
        return jsonify([])

    result_map = {}  # subject_id -> info dict (deduplicate across sections A/B)
    for cs in sections:
        timetable_entries = Timetable.query.filter_by(class_section_id=cs.id).all()
        for entry in timetable_entries:
            sid = entry.subject_id
            if sid and sid not in result_map:
                fac_name = entry.faculty.name if entry.faculty else 'Not Assigned'
                result_map[sid] = {
                    'code': entry.subject.code or '---',
                    'name': entry.subject.name,
                    'faculty': fac_name,
                    'section': cs.section,
                    'credits': entry.subject.credits,
                    'regulation': entry.subject.regulation
                }

    return jsonify(sorted(result_map.values(), key=lambda x: x['name']))

@app.route('/api/search_faculty')
def api_search_faculty():
    """Search faculty by name (partial, case-insensitive) or by numeric ID."""
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])

    # If numeric, try ID lookup first
    results = []
    if q.isdigit():
        fac = db.session.get(Faculty, int(q))
        if fac:
            results = [fac]
    if not results:
        # Partial name search
        results = Faculty.query.filter(Faculty.name.ilike(f'%{q}%')).limit(15).all()

    return jsonify([{
        'id':   f.id,
        'name': f.name,
        'department': f.department.name if f.department else '—'
    } for f in results])

@app.route('/api/faculty_by_class')
def api_faculty_by_class():
    """Returns all unique faculty members teaching in a specific branch + semester."""
    branch_id = request.args.get('branch_id')
    semester  = request.args.get('semester')

    if not branch_id or not semester:
        return jsonify([])

    sections = ClassSection.query.filter_by(branch_id=branch_id, semester=semester).all()
    faculty_map = {}  # faculty_id -> info

    for cs in sections:
        entries = Timetable.query.filter_by(class_section_id=cs.id).all()
        for entry in entries:
            if entry.faculty and entry.faculty_id not in faculty_map:
                fac = entry.faculty
                dept_name = fac.department.name if fac.department else '—'
                # Count subjects this faculty teaches in this class
                sub_names = list({e.subject.name for e in entries if e.faculty_id == fac.id and e.subject})
                faculty_map[fac.id] = {
                    'id': fac.id,
                    'name': fac.name,
                    'department': dept_name,
                    'subjects': ', '.join(sorted(sub_names))
                }

    return jsonify(sorted(faculty_map.values(), key=lambda x: x['name']))

@app.route('/api/faculty_by_dept')
def api_faculty_by_dept():
    """Returns all faculty members belonging to a specific department and their mapped subjects."""
    dept_id = request.args.get('dept_id')

    if not dept_id:
        return jsonify([])

    faculties = Faculty.query.filter_by(department_id=dept_id).all()
    result = []
    
    for fac in faculties:
        mappings = FacultySubject.query.filter_by(faculty_id=fac.id).all()
        sub_names = list({m.subject.name for m in mappings if m.subject})
        result.append({
            'id': fac.id,
            'name': fac.name,
            'department': fac.department.name if fac.department else '—',
            'subjects': ', '.join(sorted(sub_names)) if sub_names else 'Not Assigned'
        })

    return jsonify(sorted(result, key=lambda x: x['name']))

@app.route('/api/faculty_timetable/<int:faculty_id>')
def api_faculty_timetable(faculty_id):
    """Returns the complete personal timetable of a faculty member across ALL classes they teach."""
    fac = db.session.get(Faculty, faculty_id)
    if not fac:
        return jsonify({'error': 'Faculty not found'}), 404

    # Get all timetable entries for this faculty
    entries = Timetable.query.filter_by(faculty_id=faculty_id).all()

    days   = WorkingDay.query.order_by(WorkingDay.id).all()
    slots  = TimeSlot.query.order_by(TimeSlot.start_time).all()

    # Build matrix: day_name -> {slot_id: cell}
    matrix = {}
    for entry in entries:
        day_name = entry.day.day_name if entry.day else '?'
        if day_name not in matrix:
            matrix[day_name] = {}
        cs = entry.class_section
        branch = db.session.get(Branch, cs.branch_id) if cs else None
        label = f"B.Tech {branch.name if branch else '?'} S{cs.semester}{cs.section}" if cs else '?'
        is_lab = any(k in (entry.subject.name or '').lower() for k in ['lab', 'workshop', 'drawing', 'project'])
        matrix[day_name][entry.slot_id] = {
            'subject': get_abbreviation(entry.subject.name) if entry.subject else '—',
            'class':   label,
            'is_lab':  is_lab
        }

    # Serialize
    result = {
        'faculty': fac.name,
        'department': fac.department.name if fac.department else '—',
        'total_workload': fac.total_workload,
        'days':  [d.day_name for d in days],
        'slots': [{'id': s.id, 'start': s.start_time, 'end': s.end_time} for s in slots],
        'matrix': matrix
    }
    return jsonify(result)

@app.route('/api/faculty/<int:faculty_id>/assigned_sections')
@login_required
def api_faculty_assigned_sections(faculty_id):
    """Returns the class sections currently assigned to a faculty in the timetable."""
    # 1. Get from existing timetable
    entries = Timetable.query.filter_by(faculty_id=faculty_id).all()
    sections = {}
    for e in entries:
        if e.class_section and e.class_section.id not in sections:
            cs = e.class_section
            sections[cs.id] = {
                'id': cs.id,
                'label': f"B.Tech {cs.branch.name} Sem-{cs.semester} ({cs.section})"
            }

    # 2. Get from FacultySubject mappings (broader pool, no section specificity, so we have to map back to branches).
    # Since FacultySubject links to Subject, and Subject links to Department.
    # We might just pull all ClassSections where the subject is typically taught.
    # A more direct way is to fetch the current assignments if they exist. Or just list all if needed.
    # To keep it precise, we can show classes that belong to the branches where this faculty's subjects are taught.
    subjects = FacultySubject.query.filter_by(faculty_id=faculty_id).all()
    dept_ids = {s.subject.department_id for s in subjects if s.subject}
    if dept_ids:
        # Get branches for these depts
        branches = Branch.query.filter(Branch.department_id.in_(dept_ids)).all()
        branch_ids = {b.id for b in branches}
        # Get class sections for these branches
        if branch_ids:
            possible_cs = ClassSection.query.filter(ClassSection.branch_id.in_(branch_ids)).all()
            for cs in possible_cs:
                if cs.id not in sections:
                    sections[cs.id] = {
                        'id': cs.id,
                        'label': f"B.Tech {cs.branch.name} Sem-{cs.semester} ({cs.section})"
                    }

    # If the faculty has NO mappings or timetable entries, fallback to all sections
    if not sections:
        all_cs = ClassSection.query.all()
        for cs in all_cs:
            sections[cs.id] = {
                'id': cs.id,
                'label': f"B.Tech {cs.branch.name} Sem-{cs.semester} ({cs.section})"
            }
            
    # Return a sorted list based on label
    sorted_sections = sorted(list(sections.values()), key=lambda x: x['label'])
    return jsonify(sorted_sections)

# --- GENERATE TIMETABLE ---

@app.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    if request.method == 'POST':
        class_section_id = request.form.get('class_section_id') or None
        dept_id          = request.form.get('department_id')    or None
        branch_id        = request.form.get('branch_id')        or None
        semester         = request.form.get('semester')         or None

        if not class_section_id and branch_id and semester:
            sections = ClassSection.query.filter_by(branch_id=int(branch_id), semester=int(semester)).all()
            cs_ids = [cs.id for cs in sections]
        elif class_section_id:
            cs_ids = [int(class_section_id)]
        else:
            cs_ids = None

        try:
            if cs_ids:
                for cs_id in cs_ids:
                    generate_timetable(class_section_id=cs_id)
            elif dept_id:
                generate_timetable(dept_id=int(dept_id))
            else:
                generate_timetable()

            flash('✅ Timetable generated successfully using AI optimization!', 'success')
            if class_section_id:
                return redirect(url_for('view_timetable', filter_type='section', filter_id=class_section_id))
            return redirect(url_for('view_timetable'))
        except Exception as e:
            import traceback
            traceback.print_exc()
            flash(f'❌ Error generating timetable: {str(e)}', 'danger')

    departments = Department.query.all()
    return render_template('generate.html', departments=departments)

@app.route('/generate_all', methods=['POST'])
@login_required
def generate_all():
    try:
        sections = ClassSection.query.all()
        ok = 0; fail = 0
        for cs in sections:
            try:
                generate_timetable(class_section_id=cs.id)
                ok += 1
            except Exception:
                fail += 1
        flash(f'✅ Regenerated {ok} timetables. {fail} failed.', 'success' if fail == 0 else 'warning')
    except Exception as e:
        flash(f'❌ Error: {str(e)}', 'danger')
    return redirect(url_for('generate'))

# --- VIEW TIMETABLE ---
@app.route('/timetable', methods=['GET'])
@login_required
def view_timetable():
    filter_type = request.args.get('filter_type')
    filter_id = request.args.get('filter_id')

    departments = Department.query.all()
    class_section = None
    matrix = {}
    subject_faculty = []
    dept = None
    branch = None
    room_display = "---"

    if filter_type == 'section' and filter_id:
        class_section = db.session.get(ClassSection, int(filter_id))
        if class_section:
            branch = db.session.get(Branch, class_section.branch_id)
            dept = db.session.get(Department, branch.department_id)
            room_display = class_section.room_display
            
            timetable_data = Timetable.query.filter_by(class_section_id=filter_id).all()
            
            # Build matrix: {day_id: {slot_id: {abbr, faculty, is_lab}}}
            for entry in timetable_data:
                if entry.day_id not in matrix:
                    matrix[entry.day_id] = {}
                
                sub_name = entry.subject.name
                abbr = get_abbreviation(sub_name)
                is_lab = any(k in sub_name.lower() for k in ['lab', 'workshop', 'graphics', 'drawing', 'project'])
                
                matrix[entry.day_id][entry.slot_id] = {
                    'abbr': abbr,
                    'faculty': entry.faculty.name.split('(')[0].strip() if entry.faculty else '—',
                    'is_lab': is_lab
                }

            # Subject-Faculty list for footer table
            unique_subs = {}
            for entry in timetable_data:
                sid = entry.subject_id
                if sid not in unique_subs:
                    unique_subs[sid] = {
                        'subject': entry.subject,
                        'faculty': entry.faculty.name if entry.faculty else '—',
                        'abbr': get_abbreviation(entry.subject.name)
                    }
            subject_faculty = sorted(unique_subs.values(), key=lambda x: x['subject'].name)

    days = WorkingDay.query.order_by(WorkingDay.id).all()
    slots = TimeSlot.query.order_by(TimeSlot.start_time).all()

    # Helpers for vertical text breaks
    break_ltr = {'Monday': 'B', 'Tuesday': 'R', 'Wednesday': 'E', 'Thursday': 'A', 'Friday': 'K', 'Saturday': '.'}
    lunch_ltr = {'Monday': 'L', 'Tuesday': 'U', 'Wednesday': 'N', 'Thursday': 'C', 'Friday': 'H', 'Saturday': '.'}

    return render_template('timetable.html', 
                          departments=departments,
                          class_section=class_section,
                          dept=dept,
                          branch=branch,
                          room_display=room_display,
                          matrix=matrix,
                          days=days,
                          slots=slots,
                          subject_faculty=subject_faculty,
                          break_ltr=break_ltr,
                          lunch_ltr=lunch_ltr,
                          today=date.today().strftime('%d-%m-%Y'))

@app.route('/student', methods=['GET'])
def student_portal():
    filter_type = request.args.get('filter_type')
    filter_id = request.args.get('filter_id')

    departments = Department.query.all()
    class_section = None
    matrix = {}
    subject_faculty = []
    dept = None
    branch = None
    room_display = "---"

    if filter_type == 'section' and filter_id:
        class_section = db.session.get(ClassSection, int(filter_id))
        if class_section:
            branch = db.session.get(Branch, class_section.branch_id)
            dept = db.session.get(Department, branch.department_id)
            room_display = class_section.room_display
            
            timetable_data = Timetable.query.filter_by(class_section_id=filter_id).all()
            
            # Build matrix: {day_id: {slot_id: {abbr, faculty, is_lab}}}
            for entry in timetable_data:
                if entry.day_id not in matrix:
                    matrix[entry.day_id] = {}
                
                sub_name = entry.subject.name
                abbr = get_abbreviation(sub_name)
                is_lab = any(k in sub_name.lower() for k in ['lab', 'workshop', 'graphics', 'drawing', 'project'])
                
                matrix[entry.day_id][entry.slot_id] = {
                    'abbr': abbr,
                    'faculty': entry.faculty.name.split('(')[0].strip() if entry.faculty else '—',
                    'is_lab': is_lab
                }

            # Subject-Faculty list for footer table
            unique_subs = {}
            for entry in timetable_data:
                sid = entry.subject_id
                if sid not in unique_subs:
                    unique_subs[sid] = {
                        'subject': entry.subject,
                        'faculty': entry.faculty.name if entry.faculty else '—',
                        'abbr': get_abbreviation(entry.subject.name)
                    }
            subject_faculty = sorted(unique_subs.values(), key=lambda x: x['subject'].name)

    days = WorkingDay.query.order_by(WorkingDay.id).all()
    slots = TimeSlot.query.order_by(TimeSlot.start_time).all()

    break_ltr = {'Monday': 'B', 'Tuesday': 'R', 'Wednesday': 'E', 'Thursday': 'A', 'Friday': 'K', 'Saturday': '.'}
    lunch_ltr = {'Monday': 'L', 'Tuesday': 'U', 'Wednesday': 'N', 'Thursday': 'C', 'Friday': 'H', 'Saturday': '.'}

    return render_template('student.html', 
                          departments=departments,
                          faculty_list=Faculty.query.order_by(Faculty.name).all(),
                          class_section=class_section,
                          dept=dept,
                          branch=branch,
                          room_display=room_display,
                          matrix=matrix,
                          days=days,
                          slots=slots,
                          subject_faculty=subject_faculty,
                          break_ltr=break_ltr,
                          lunch_ltr=lunch_ltr,
                          today=date.today().strftime('%d-%m-%Y'))

if __name__ == '__main__':
    app.run(debug=True)
