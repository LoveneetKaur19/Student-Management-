from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()


# ==========================================================
# USER TABLE
# ==========================================================

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)


# ==========================================================
# STUDENT TABLE
# ==========================================================

class Students(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    roll_number = db.Column(db.String(20), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)

    branch = db.Column(db.String(100), nullable=False)

    semester = db.Column(db.String(20), nullable=False)

    phone = db.Column(db.String(15))

    email = db.Column(db.String(120), unique=True)

    photo = db.Column(db.String(255))

    marks = db.Column(db.Float, default=0)

    attendance = db.Column(db.Float, default=0)

    total_fee = db.Column(db.Float, default=0)

    paid_fee = db.Column(db.Float, default=0)

    due_fee = db.Column(db.Float, default=0)

    fee_status = db.Column(db.String(20), default="Pending")

    status = db.Column(db.String(30), default="Active")

    admission_date = db.Column(
        db.Date,
        default=date.today
    )


# ==========================================================
# SUBJECT TABLE
# ==========================================================

class Subject(db.Model):

    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)

    subject_name = db.Column(
        db.String(100),
        nullable=False
    )

    subject_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    credits = db.Column(db.Integer)


# ==========================================================
# ENROLLMENT TABLE
# ==========================================================

class Enrollment(db.Model):

    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )

    student = db.relationship(
        "Students",
        backref="enrollments"
    )

    subject = db.relationship(
        "Subject",
        backref="enrollments"
    )


# ==========================================================
# ATTENDANCE TABLE
# ==========================================================

class Attendance(db.Model):

    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )

    attendance_date = db.Column(
        db.Date,
        default=date.today
    )

    status = db.Column(
        db.String(20),
        nullable=False
    )

    student = db.relationship(
        "Students",
        backref="attendance_records"
    )

    subject = db.relationship(
        "Subject",
        backref="attendance_records"
    )


# ==========================================================
# MARKS TABLE
# ==========================================================

class Marks(db.Model):

    __tablename__ = "marks"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )

    internal_marks = db.Column(
        db.Float,
        default=0
    )

    external_marks = db.Column(
        db.Float,
        default=0
    )

    total_marks = db.Column(
        db.Float,
        default=0
    )

    grade = db.Column(
        db.String(5)
    )

    result = db.Column(
        db.String(20)
    )

    student = db.relationship(
        "Students",
        backref="marks_records"
    )

    subject = db.relationship(
        "Subject",
        backref="marks_records"
    )


# ==========================================================
# FEE PAYMENT TABLE
# ==========================================================

class FeePayment(db.Model):

    __tablename__ = "fee_payments"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    payment_date = db.Column(
        db.Date,
        default=date.today
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    payment_mode = db.Column(
        db.String(30)
    )

    receipt_number = db.Column(
        db.String(100),
        unique=True
    )

    student = db.relationship(
        "Students",
        backref="fee_payments"
    )


# ==========================================================
# ASSIGNMENT TABLE
# ==========================================================

class Assignment(db.Model):

    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )

    description = db.Column(db.Text)

    due_date = db.Column(db.Date)

    file_name = db.Column(
        db.String(255)
    )

    subject = db.relationship(
        "Subject",
        backref="assignments"
    )


# ==========================================================
# LEAVE TABLE
# ==========================================================

class Leave(db.Model):

    __tablename__ = "leave"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    from_date = db.Column(db.Date)

    to_date = db.Column(db.Date)

    reason = db.Column(db.Text)

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    student = db.relationship(
        "Students",
        backref="leave_records"
    )