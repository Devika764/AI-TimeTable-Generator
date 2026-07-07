from app import app, db
from models import Timetable, Subject, Faculty, Classroom, WorkingDay, TimeSlot

with app.app_context():
    timetables = Timetable.query.all()
    
    # 1. Faculty Conflicts
    faculty_slots = {}
    faculty_conflicts = 0
    for tt in timetables:
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
    print(f"Faculty conflicts: {faculty_conflicts}")
    print(f"Room conflicts: {room_conflicts}")
    
    # Check for LIBRARY
    lib_count = Timetable.query.join(Subject).filter(Subject.name == 'LIBRARY').count()
    print(f"LIBRARY sessions forced: {lib_count}")
