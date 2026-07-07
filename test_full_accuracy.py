import os
from app import app
from models import db, FacultyPreferredSlot, Timetable, Department
from ai_module import generate_timetable

def test_full_accuracy():
    with app.app_context():
        print("Regenerating ALL sections...")
        from models import ClassSection
        sections = ClassSection.query.all()
        for cs in sections:
            try:
                generate_timetable(class_section_id=cs.id)
            except Exception as e:
                db.session.rollback()
                print(f"Failed CS {cs.id}: {e}")
        
        prefs = FacultyPreferredSlot.query.all()
        print(f"Total Prefs defined: {len(prefs)}")
        
        accuracy = 0
        for p in prefs:
            entries = []
            if p.class_section_id:
                entries = Timetable.query.filter_by(
                    faculty_id=p.faculty_id,
                    day_id=p.day_id,
                    slot_id=p.slot_id,
                    class_section_id=p.class_section_id
                ).all()
            else:
                entries = Timetable.query.filter_by(
                    faculty_id=p.faculty_id,
                    day_id=p.day_id,
                    slot_id=p.slot_id
                ).all()

            if entries:
                accuracy += 1
                if p.class_section_id:
                     print(f"[OK] Faculty {p.faculty.name} is scheduled on Day {p.day_id} Slot {p.slot_id} in required class {p.class_section_id}.")
                else:
                     print(f"[OK] Faculty {p.faculty.name} is scheduled on Day {p.day_id} Slot {p.slot_id} in {len(entries)} classes.")
            else:
                print(f"[FAIL] Faculty {p.faculty.name} is MISSING from Day {p.day_id} Slot {p.slot_id}! Accuracy failed.")
                
        print(f"Accuracy: {accuracy}/{len(prefs)}")

if __name__ == '__main__':
    test_full_accuracy()
