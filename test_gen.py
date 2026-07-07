from app import app
from models import *
from ai_module import generate_timetable

with app.app_context():
    ok = 0
    fail = 0
    for cs in ClassSection.query.all():
        try:
            generate_timetable(class_section_id=cs.id)
            ok += 1
        except Exception as e:
            db.session.rollback()
            fail += 1
            print(f"Failed CS {cs.id}: {e}")
    print(f"OK: {ok}, FAIL: {fail}")
