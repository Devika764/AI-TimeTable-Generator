import os
from app import app, db
from models import Department, Subject, Faculty, FacultySubject, Classroom, WorkingDay, TimeSlot

semesters_data = [
    {"name": "1st Sem - AIML", "code_prefix": "S1", "theory": 5, "labs": 4, "internship": 0, "faculty": 6},
    {"name": "2nd Sem - AIML", "code_prefix": "S2", "theory": 5, "labs": 3, "internship": 0, "faculty": 5},
    {"name": "3rd Sem - AIML", "code_prefix": "S3", "theory": 6, "labs": 4, "internship": 0, "faculty": 6},
    {"name": "4th Sem - AIML", "code_prefix": "S4", "theory": 5, "labs": 4, "internship": 0, "faculty": 6},
    {"name": "5th Sem - AIML", "code_prefix": "S5", "theory": 6, "labs": 3, "internship": 0, "faculty": 6},
    {"name": "6th Sem - AIML", "code_prefix": "S6", "theory": 5, "labs": 4, "internship": 1, "faculty": 6},
    {"name": "7th Sem - AIML", "code_prefix": "S7", "theory": 6, "labs": 1, "internship": 0, "faculty": 6},
]

with app.app_context():
    # Make sure we have classrooms
    if Classroom.query.count() == 0:
        for i in range(1, 11):
            db.session.add(Classroom(name=f"Room {i}", capacity=60))
        db.session.commit()

    # Time slots
    if TimeSlot.query.count() == 0:
        slots = [
            ("09:00", "10:00"), ("10:00", "11:00"), ("11:00", "12:00"),
            ("13:00", "14:00"), ("14:00", "15:00"), ("15:00", "16:00"), ("16:00", "17:00")
        ]
        for s, e in slots:
            db.session.add(TimeSlot(start_time=s, end_time=e))
        db.session.commit()

    for sem_data in semesters_data:
        dept = Department.query.filter_by(name=sem_data['name']).first()
        if not dept:
            dept = Department(name=sem_data['name'])
            db.session.add(dept)
            db.session.commit()
            
        print(f"Populating {dept.name} with subjects and faculty...")
        
        # Add faculty
        for i in range(1, sem_data['faculty'] + 1):
            fac_name = f"Faculty {sem_data['code_prefix']}-{i}"
            if not Faculty.query.filter_by(name=fac_name, department_id=dept.id).first():
                fac = Faculty(name=fac_name, department_id=dept.id)
                db.session.add(fac)
        db.session.commit()
        
        # Add classes
        # Theory
        prefix = sem_data['code_prefix']
        for i in range(1, sem_data['theory'] + 1):
            code = f"{prefix}-TH{i}"
            name = f"Theory Subject {i}"
            if not Subject.query.filter_by(code=code, department_id=dept.id).first():
                sub = Subject(code=code, name=name, department_id=dept.id, hours_per_week=3)
                db.session.add(sub)
                
        # Labs
        for i in range(1, sem_data['labs'] + 1):
            code = f"{prefix}-LAB{i}"
            name = f"Lab Subject {i}"
            if not Subject.query.filter_by(code=code, department_id=dept.id).first():
                sub = Subject(code=code, name=name, department_id=dept.id, hours_per_week=3)
                db.session.add(sub)
                
        # Internship
        for i in range(1, sem_data['internship'] + 1):
            code = f"{prefix}-INT{i}"
            name = f"Internship {i}"
            if not Subject.query.filter_by(code=code, department_id=dept.id).first():
                sub = Subject(code=code, name=name, department_id=dept.id, hours_per_week=2)
                db.session.add(sub)
                
        db.session.commit()
        
        dept_faculties = Faculty.query.filter_by(department_id=dept.id).all()
        dept_subjects = Subject.query.filter_by(department_id=dept.id).all()
        
        # Assign subjects to faculty
        for idx, sub in enumerate(dept_subjects):
            assigned_fac = dept_faculties[idx % len(dept_faculties)]
            if not FacultySubject.query.filter_by(faculty_id=assigned_fac.id, subject_id=sub.id).first():
                fs = FacultySubject(faculty_id=assigned_fac.id, subject_id=sub.id)
                db.session.add(fs)
        db.session.commit()
    
    print("Seeding completed.")
