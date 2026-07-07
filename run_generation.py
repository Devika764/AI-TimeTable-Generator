from app import app, db
from models import ClassSection, Timetable
from ai_module import generate_timetable

with app.app_context():
    print("Deleting old timetables...")
    Timetable.query.delete()
    db.session.commit()
    
    sections = ClassSection.query.all()
    print(f"Generating new timetables for {len(sections)} sections...")
    
    success_count = 0
    for i, cs in enumerate(sections, 1):
        try:
            generate_timetable(class_section_id=cs.id)
            success_count += 1
            if i % 10 == 0:
                print(f"Generated {i}/{len(sections)} timetables ({(i/len(sections)*100):.1f}%)")
        except Exception as e:
            print(f"Failed to generate for section {cs.id}: {e}")
            
    print(f"\nSuccessfully generated {success_count}/{len(sections)} timetables!")
