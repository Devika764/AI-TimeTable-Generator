from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    subjects = db.relationship('Subject', backref='department', lazy=True, cascade='all, delete-orphan')
    faculty = db.relationship('Faculty', backref='department', lazy=True, cascade='all, delete-orphan')
    branches = db.relationship('Branch', backref='department', lazy=True, cascade='all, delete-orphan')

# Branch belongs to a Department (e.g., AIML, AIDS under AI; CSE under CSE)
class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)           # e.g., AIML, AIDS, CSE, IT, ECE, EEE
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    sections = db.relationship('ClassSection', backref='branch', lazy=True, cascade='all, delete-orphan')

# ClassSection = Branch + Semester + Section letter (e.g., AIML Sem-1 Section A)
class ClassSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)
    semester = db.Column(db.Integer, nullable=False)           # 1–8
    section = db.Column(db.String(5), nullable=False)          # A, B, or C

    @property
    def sem_roman(self):
        vals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
        return vals[self.semester-1] if 1 <= self.semester <= 8 else str(self.semester)

    @property
    def year_roman(self):
        # 1-2=I, 3-4=II, 5-6=III, 7-8=IV
        vals = ['I', 'I', 'II', 'II', 'III', 'III', 'IV', 'IV']
        return vals[self.semester-1] if 1 <= self.semester <= 8 else '?'

    @property
    def room_display(self):
        # Find the first timetable entry to see which room is assigned (or derived from ID)
        tt = Timetable.query.filter_by(class_section_id=self.id).first()
        if tt and tt.classroom:
            return tt.classroom.name
        return "TBD"

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    semester = db.Column(db.Integer, nullable=True)
    hours_per_week = db.Column(db.Integer, nullable=False)
    subject_type = db.Column(db.String(20), nullable=False, server_default='Theory')
    credits = db.Column(db.Float, nullable=False, server_default='3.0')
    regulation = db.Column(db.String(50), nullable=False, server_default='R20')

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    
    @property
    def assigned_classes(self):
        """Returns a list of unique class labels (Branch Sem Section) this faculty teaches."""
        # Note: Timetable is defined later, so we use string-based query or import inside
        from models import Timetable
        entries = Timetable.query.filter_by(faculty_id=self.id).all()
        class_sections = set()
        for e in entries:
            if e.class_section:
                cs = e.class_section
                label = f"B.Tech {cs.branch.name} Sem-{cs.semester} ({cs.section})"
                class_sections.add(label)
        return sorted(list(class_sections))

    @property
    def total_workload(self):
        """Returns the total scheduled hours per week for this faculty."""
        from models import Timetable
        return Timetable.query.filter_by(faculty_id=self.id).count()


class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

class WorkingDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_name = db.Column(db.String(20), unique=True, nullable=False) # e.g., Monday, Tuesday

class TimeSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String(10), nullable=False) # e.g., 09:00 AM
    end_time = db.Column(db.String(10), nullable=False) # e.g., 10:00 AM

# Many-to-Many relationship between Faculty and Subjects
class FacultySubject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)

    faculty = db.relationship('Faculty')
    subject = db.relationship('Subject')

# Many-to-Many mapping for preferred slots (Soft constraint)
class FacultyPreferredSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id', ondelete='CASCADE'), nullable=False)
    class_section_id = db.Column(db.Integer, db.ForeignKey('class_section.id', ondelete='CASCADE'), nullable=True)
    day_id = db.Column(db.Integer, db.ForeignKey('working_day.id', ondelete='CASCADE'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('time_slot.id', ondelete='CASCADE'), nullable=False)

    faculty = db.relationship('Faculty')
    class_section = db.relationship('ClassSection')
    day     = db.relationship('WorkingDay')
    slot    = db.relationship('TimeSlot')

class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_section_id = db.Column(db.Integer, db.ForeignKey('class_section.id', ondelete='CASCADE'), nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('working_day.id'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('time_slot.id'), nullable=False)

    class_section = db.relationship('ClassSection')

    subject = db.relationship('Subject')
    faculty = db.relationship('Faculty')
    classroom = db.relationship('Classroom')
    day = db.relationship('WorkingDay')
    slot = db.relationship('TimeSlot')
