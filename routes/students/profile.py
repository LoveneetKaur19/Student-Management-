from flask import render_template, session, redirect

from app import app

from models import (
    Students,
    Enrollment,
    Attendance,
    Marks,
    FeePayment,
    Leave
)


@app.route("/student_profile/<int:id>")
def student_profile(id):

    # Login check
    if "user_id" not in session:
        return redirect("/login")

    # Student
    student = Students.query.get_or_404(id)

    # =====================================
    # STUDENT RANK
    # =====================================

    students = Students.query.order_by(
        Students.marks.desc()
    ).all()

    rank = 1

    for s in students:

        if s.id == student.id:
            break

        rank += 1

    # =====================================
    # ENROLLED SUBJECTS
    # =====================================

    enrollments = Enrollment.query.filter_by(
        student_id=student.id
    ).all()

    # =====================================
    # ATTENDANCE RECORDS
    # =====================================

    attendance_records = Attendance.query.filter_by(
        student_id=student.id
    ).order_by(
        Attendance.attendance_date.desc()
    ).all()

    # =====================================
    # MARKS RECORDS
    # =====================================

    marks_records = Marks.query.filter_by(
        student_id=student.id
    ).all()

    # =====================================
    # FEE PAYMENT HISTORY
    # =====================================

    fee_payments = FeePayment.query.filter_by(
        student_id=student.id
    ).order_by(
        FeePayment.payment_date.desc()
    ).all()

    # =====================================
    # LEAVE HISTORY
    # =====================================

    leave_records = Leave.query.filter_by(
        student_id=student.id
    ).order_by(
        Leave.id.desc()
    ).all()

    # =====================================
    # RENDER PROFILE
    # =====================================

    return render_template(

        "student_profile.html",

        student=student,

        rank=rank,

        total_students=len(students),

        enrollments=enrollments,

        attendance_records=attendance_records,

        marks_records=marks_records,

        fee_payments=fee_payments,

        leave_records=leave_records

    )