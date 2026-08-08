from flask import (
    render_template,
    request,
    redirect,
    session,
    flash
)

from app import app
from models import (
    db,
    Students,
    Subject,
    Enrollment
)


# =====================================
# Add Enrollment
# =====================================

@app.route("/add_enrollment", methods=["GET", "POST"])
def add_enrollment():

    if "user_id" not in session:
        return redirect("/login")

    students = Students.query.order_by(Students.name).all()
    subjects = Subject.query.order_by(Subject.subject_name).all()

    if request.method == "POST":

        student_id = request.form["student_id"]
        subject_id = request.form["subject_id"]

        existing = Enrollment.query.filter_by(
            student_id=student_id,
            subject_id=subject_id
        ).first()

        if existing:
            flash("Student is already enrolled in this subject.", "warning")
            return redirect("/add_enrollment")

        enrollment = Enrollment(
            student_id=student_id,
            subject_id=subject_id
        )

        db.session.add(enrollment)
        db.session.commit()

        flash("Enrollment Added Successfully!", "success")

        return redirect("/view_enrollments")

    return render_template(
        "add_enrollment.html",
        students=students,
        subjects=subjects
    )


# =====================================
# View Enrollment
# =====================================

@app.route("/view_enrollments")
def view_enrollments():

    if "user_id" not in session:
        return redirect("/login")

    enrollments = Enrollment.query.all()

    return render_template(
        "view_enrollments.html",
        enrollments=enrollments
    )


# =====================================
# Delete Enrollment
# =====================================

@app.route("/delete_enrollment/<int:id>")
def delete_enrollment(id):

    if "user_id" not in session:
        return redirect("/login")

    enrollment = Enrollment.query.get_or_404(id)

    db.session.delete(enrollment)

    db.session.commit()

    flash(
        "Enrollment Deleted Successfully!",
        "success"
    )

    return redirect("/view_enrollments")