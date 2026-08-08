from flask import (
    render_template,
    request,
    redirect,
    session,
    flash
)

from datetime import datetime

from app import app
from models import (
    db,
    Students,
    Subject,
    Attendance
)


# =====================================
# Add Attendance
# =====================================

@app.route("/add_attendance", methods=["GET", "POST"])
def add_attendance():

    if "user_id" not in session:
        return redirect("/login")

    students = Students.query.order_by(Students.name).all()
    subjects = Subject.query.order_by(Subject.subject_name).all()

    if request.method == "POST":

        student_id = request.form["student_id"]
        subject_id = request.form["subject_id"]

        attendance_date = datetime.strptime(
            request.form["attendance_date"],
            "%Y-%m-%d"
        ).date()

        status = request.form["status"]

        attendance = Attendance(

            student_id=student_id,

            subject_id=subject_id,

            attendance_date=attendance_date,

            status=status

        )

        db.session.add(attendance)

        db.session.commit()

        flash(
            "Attendance Added Successfully!",
            "success"
        )

        return redirect("/view_attendance")

    return render_template(
        "add_attendance.html",
        students=students,
        subjects=subjects
    )


# =====================================
# View Attendance
# =====================================

@app.route("/view_attendance")
def view_attendance():

    if "user_id" not in session:
        return redirect("/login")

    attendance = Attendance.query.order_by(
        Attendance.attendance_date.desc()
    ).all()

    return render_template(
        "view_attendance.html",
        attendance=attendance
    )


# =====================================
# Update Attendance
# =====================================

@app.route("/update_attendance/<int:id>", methods=["GET", "POST"])
def update_attendance(id):

    if "user_id" not in session:
        return redirect("/login")

    attendance = Attendance.query.get_or_404(id)

    students = Students.query.order_by(
        Students.name
    ).all()

    subjects = Subject.query.order_by(
        Subject.subject_name
    ).all()

    if request.method == "POST":

        attendance.student_id = request.form["student_id"]

        attendance.subject_id = request.form["subject_id"]

        attendance.attendance_date = datetime.strptime(
            request.form["attendance_date"],
            "%Y-%m-%d"
        ).date()

        attendance.status = request.form["status"]

        db.session.commit()

        flash(
            "Attendance Updated Successfully!",
            "success"
        )

        return redirect("/view_attendance")

    return render_template(
        "update_attendance.html",
        attendance=attendance,
        students=students,
        subjects=subjects
    )


# =====================================
# Delete Attendance
# =====================================

@app.route("/delete_attendance/<int:id>")
def delete_attendance(id):

    if "user_id" not in session:
        return redirect("/login")

    record = Attendance.query.get_or_404(id)

    db.session.delete(record)

    db.session.commit()

    flash(
        "Attendance Deleted Successfully!",
        "success"
    )

    return redirect("/view_attendance")