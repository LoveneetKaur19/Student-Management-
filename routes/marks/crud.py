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
    Marks
)


# =====================================
# Add Marks
# =====================================

@app.route("/add_marks", methods=["GET", "POST"])
def add_marks():

    if "user_id" not in session:
        return redirect("/login")

    students = Students.query.order_by(
        Students.name
    ).all()

    subjects = Subject.query.order_by(
        Subject.subject_name
    ).all()

    if request.method == "POST":

        student_id = request.form["student_id"]
        subject_id = request.form["subject_id"]

        internal = float(request.form["internal_marks"])
        external = float(request.form["external_marks"])

        total = internal + external

        if total >= 90:
            grade = "A+"
            result = "Pass"

        elif total >= 80:
            grade = "A"
            result = "Pass"

        elif total >= 70:
            grade = "B"
            result = "Pass"

        elif total >= 60:
            grade = "C"
            result = "Pass"

        elif total >= 40:
            grade = "D"
            result = "Pass"

        else:
            grade = "F"
            result = "Fail"

        mark = Marks(

            student_id=student_id,

            subject_id=subject_id,

            internal_marks=internal,

            external_marks=external,

            total_marks=total,

            grade=grade,

            result=result

        )

        db.session.add(mark)

        db.session.commit()

        flash(
            "Marks Added Successfully!",
            "success"
        )

        return redirect("/view_marks")

    return render_template(
        "add_marks.html",
        students=students,
        subjects=subjects
    )


# =====================================
# View Marks
# =====================================

@app.route("/view_marks")
def view_marks():

    if "user_id" not in session:
        return redirect("/login")

    marks = Marks.query.all()

    return render_template(
        "view_marks.html",
        marks=marks
    )


# =====================================
# Update Marks
# =====================================

@app.route("/update_marks/<int:id>", methods=["GET", "POST"])
def update_marks(id):

    if "user_id" not in session:
        return redirect("/login")

    mark = Marks.query.get_or_404(id)

    students = Students.query.order_by(
        Students.name
    ).all()

    subjects = Subject.query.order_by(
        Subject.subject_name
    ).all()

    if request.method == "POST":

        mark.student_id = request.form["student_id"]
        mark.subject_id = request.form["subject_id"]

        internal = float(request.form["internal_marks"])
        external = float(request.form["external_marks"])

        # Validation
        if internal < 0 or internal > 30:
            flash("Internal Marks must be between 0 and 30.", "danger")
            return redirect(f"/update_marks/{id}")

        if external < 0 or external > 70:
            flash("External Marks must be between 0 and 70.", "danger")
            return redirect(f"/update_marks/{id}")

        total = internal + external

        if total >= 90:
            grade = "A+"
            result = "Pass"
        elif total >= 80:
            grade = "A"
            result = "Pass"
        elif total >= 70:
            grade = "B"
            result = "Pass"
        elif total >= 60:
            grade = "C"
            result = "Pass"
        elif total >= 40:
            grade = "D"
            result = "Pass"
        else:
            grade = "F"
            result = "Fail"

        mark.internal_marks = internal
        mark.external_marks = external
        mark.total_marks = total
        mark.grade = grade
        mark.result = result

        db.session.commit()

        flash(
            "Marks Updated Successfully!",
            "success"
        )

        return redirect("/view_marks")

    return render_template(
        "update_marks.html",
        mark=mark,
        students=students,
        subjects=subjects
    )


# =====================================
# Delete Marks
# =====================================

@app.route("/delete_marks/<int:id>")
def delete_marks(id):

    if "user_id" not in session:
        return redirect("/login")

    mark = Marks.query.get_or_404(id)

    db.session.delete(mark)

    db.session.commit()

    flash(
        "Marks Deleted Successfully!",
        "success"
    )

    return redirect("/view_marks")