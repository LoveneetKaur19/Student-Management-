from flask import (
    render_template,
    request,
    redirect,
    session,
    flash
)

from werkzeug.utils import secure_filename

from app import app
from models import db, Students

import os


# -------------------------------
# Helper Function
# -------------------------------

def calculate_status(marks, attendance):

    if marks >= 85 and attendance >= 90:
        return "Excellent"

    elif marks >= 70:
        return "Good"

    elif marks >= 50:
        return "Average"

    else:
        return "Needs Improvement"


# -------------------------------
# Add Student
# -------------------------------

@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        roll_number = request.form["roll_number"].strip()
        name = request.form["name"].strip()
        branch = request.form["branch"]
        semester = request.form["semester"]
        phone = request.form["phone"]
        email = request.form["email"].strip().lower()

        marks = float(request.form["marks"])
        attendance = float(request.form["attendance"])

        total_fee = float(request.form["total_fee"])
        paid_fee = float(request.form["paid_fee"])

        # ---------------- Validation ----------------

        if Students.query.filter_by(
                roll_number=roll_number).first():

            flash("Roll Number already exists.", "danger")
            return redirect("/add_student")

        if Students.query.filter_by(
                email=email).first():

            flash("Email already exists.", "danger")
            return redirect("/add_student")

        if not (0 <= marks <= 100):

            flash("Marks must be between 0 and 100.", "danger")
            return redirect("/add_student")

        if not (0 <= attendance <= 100):

            flash("Attendance must be between 0 and 100.", "danger")
            return redirect("/add_student")

        if paid_fee > total_fee:

            flash("Paid Fee cannot be greater than Total Fee.", "danger")
            return redirect("/add_student")

        due_fee = total_fee - paid_fee

        fee_status = "Paid"

        if due_fee > 0:
            fee_status = "Pending"

        student_status = calculate_status(
            marks,
            attendance
        )


        # ---------------- Photo ----------------

        filename = "default.png"

        photo = request.files.get("photo")

        if photo and photo.filename != "":

            filename = secure_filename(photo.filename)

            photo.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        # ---------------- Database ----------------

        student = Students(

            roll_number=roll_number,

            name=name,

            branch=branch,

            semester=semester,

            phone=phone,

            email=email,

            marks=marks,

            attendance=attendance,

            status=student_status,

            photo=filename,

            total_fee=total_fee,

            paid_fee=paid_fee,

            due_fee=due_fee,

            fee_status=fee_status

        )

        db.session.add(student)

        db.session.commit()

        flash(
            "Student Added Successfully!",
            "success"
        )

        return redirect("/view_students")

    return render_template("add_student.html")


# ---------------------------------------
# View Students
# ---------------------------------------

@app.route("/view_students")
def view_students():

    if "user_id" not in session:
        return redirect("/login")

    students = Students.query.order_by(
        Students.id.desc()
    ).all()

    return render_template(
        "view_students.html",
        students=students
    )


# ---------------------------------------
# Delete Student
# ---------------------------------------

@app.route("/delete_student/<int:id>")
def delete_student(id):

    if "user_id" not in session:
        return redirect("/login")

    student = Students.query.get_or_404(id)

    # Delete photo (except default)
    if student.photo and student.photo != "default.png":

        photo_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            student.photo
        )

        if os.path.exists(photo_path):
            os.remove(photo_path)

    db.session.delete(student)
    db.session.commit()

    flash(
        "Student Deleted Successfully!",
        "success"
    )

    return redirect("/view_students")


# ---------------------------------------
# Update Student
# ---------------------------------------

@app.route("/update_student/<int:id>", methods=["GET", "POST"])
def update_student(id):

    if "user_id" not in session:
        return redirect("/login")

    student = Students.query.get_or_404(id)

    if request.method == "POST":

        student.roll_number = request.form["roll_number"]
        student.name = request.form["name"]
        student.branch = request.form["branch"]
        student.semester = request.form["semester"]
        student.phone = request.form["phone"]
        student.email = request.form["email"]

        student.marks = float(request.form["marks"])
        student.attendance = float(request.form["attendance"])

        student.total_fee = float(request.form["total_fee"])
        student.paid_fee = float(request.form["paid_fee"])

        student.due_fee = (
            student.total_fee -
            student.paid_fee
        )

        student.fee_status = (
            "Paid"
            if student.due_fee == 0
            else "Pending"
        )

        student.status = calculate_status(
            student.marks,
            student.attendance
        )

        photo = request.files.get("photo")

        if photo and photo.filename != "":

            filename = secure_filename(photo.filename)

            photo.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            student.photo = filename

        db.session.commit()

        flash(
            "Student Updated Successfully!",
            "success"
        )

        return redirect("/view_students")

    return render_template(
        "update_student.html",
        student=student
    )

