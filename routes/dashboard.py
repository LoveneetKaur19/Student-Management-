from flask import render_template, session, redirect
from app import app
from models import (
    Students,
    Subject,
    Enrollment,
    Attendance,
    Assignment,
    Leave,db
)


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    # ==========================
    # Statistics
    # ==========================

    total_students = Students.query.count()

    total_subjects = Subject.query.count()
    total_branches = db.session.query(
        Students.branch
    ).distinct().count()

    branch_data = {}

    students = Students.query.all()

    for student in students:

        if student.branch in branch_data:

            branch_data[student.branch] += 1

        else:

            branch_data[student.branch] = 1


    total_enrollments = Enrollment.query.count()

    total_attendance = Attendance.query.count()

    total_assignments = Assignment.query.count()

    pending_leaves = Leave.query.filter_by(
        status="Pending"
    ).count()


# ==========================
# Top Student
# ==========================

    top_student = Students.query.order_by(
        Students.marks.desc()
    ).first()

    total_fee = sum(
        student.total_fee or 0
        for student in students
    )


    total_fee_collected = sum(
        student.paid_fee or 0
        for student in students
    )

    total_due_fee = sum(
        student.due_fee or 0
        for student in students
    )

    recent_leaves = Leave.query.order_by(
        Leave.id.desc()
    ).limit(5).all()


    return render_template(

        "dashboard.html",

        total_students=total_students,

        total_subjects=total_subjects,

        total_branches=total_branches,
        branch_data=branch_data,

        total_enrollments=total_enrollments,

        total_attendance=total_attendance,

        total_assignments=total_assignments,
        recent_leaves=recent_leaves,
        pending_leaves=pending_leaves,
        top_student=top_student,

        total_fee_collected=total_fee_collected,
        total_fee=total_fee,
        total_due_fee=total_due_fee,

        recent_students=Students.query.order_by(
            Students.id.desc()
        ).limit(5).all(),

        fee_defaulters=Students.query.filter(
            Students.due_fee > 0
        ).order_by(
            Students.due_fee.desc()
        ).limit(5).all(),

    )