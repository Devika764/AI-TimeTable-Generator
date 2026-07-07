from app import app, db
from models import Timetable, Subject, Faculty, Classroom, WorkingDay, TimeSlot

with app.app_context():
    timetables = Timetable.query.all()
    
    # Check for LIBRARY
    lib_subj = Subject.query.filter_by(name='LIBRARY').first()
    lib_fac = Faculty.query.filter_by(name='Self Study').first()
    lib_subj_id = lib_subj.id if lib_subj else -1
    lib_fac_id = lib_fac.id if lib_fac else -1

    # 1. Faculty Conflicts
    faculty_slots = {}
    faculty_conflicts = 0
    for tt in timetables:
        if tt.faculty_id == lib_fac_id:
            continue
        key = (tt.day_id, tt.slot_id, tt.faculty_id)
        if key in faculty_slots:
            faculty_conflicts += 1
        faculty_slots[key] = True

    # 2. Room Conflicts
    room_slots = {}
    room_conflicts = 0
    for tt in timetables:
        key = (tt.day_id, tt.slot_id, tt.classroom_id)
        if key in room_slots:
            room_conflicts += 1
        room_slots[key] = True

    print(f"Total entries: {len(timetables)}")
    print(f"REAL Faculty conflicts: {faculty_conflicts}")
    print(f"Room conflicts: {room_conflicts}")
    print(f"LIBRARY sessions forced: {len([t for t in timetables if t.subject_id == lib_subj_id])}")
