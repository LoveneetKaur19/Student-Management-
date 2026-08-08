from flask import (
    render_template,
    request,
    redirect,
    session,
    flash
)

from app import app
from models import db, Subject


# =====================================
# Add Subject
# =====================================

@app.route("/add_subject", methods=["GET", "POST"])
def add_subject():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        subject_name = request.form["subject_name"].strip()

        subject_code = request.form["subject_code"].strip().upper()

        credits = int(request.form["credits"])

        existing = Subject.query.filter_by(
            subject_code=subject_code
        ).first()

        if existing:

            flash(
                "Subject Code Already Exists!",
                "danger"
            )

            return redirect("/add_subject")

        subject = Subject(

            subject_name=subject_name,

            subject_code=subject_code,

            credits=credits

        )

        db.session.add(subject)

        db.session.commit()

        flash(
            "Subject Added Successfully!",
            "success"
        )

        return redirect("/view_subjects")

    return render_template(
        "add_subject.html"
    )


# =====================================
# View Subjects
# =====================================

@app.route("/view_subjects")
def view_subjects():

    if "user_id" not in session:
        return redirect("/login")

    subjects = Subject.query.order_by(
        Subject.id.desc()
    ).all()

    return render_template(
        "view_subjects.html",
        subjects=subjects
    )


# =====================================
# Update Subject
# =====================================

@app.route("/update_subject/<int:id>",
           methods=["GET", "POST"])
def update_subject(id):

    if "user_id" not in session:
        return redirect("/login")

    subject = Subject.query.get_or_404(id)

    if request.method == "POST":

        subject.subject_name = request.form["subject_name"]

        subject.subject_code = request.form["subject_code"]

        subject.credits = int(
            request.form["credits"]
        )

        db.session.commit()

        flash(
            "Subject Updated Successfully!",
            "success"
        )

        return redirect("/view_subjects")

    return render_template(
        "update_subject.html",
        subject=subject
    )


# =====================================
# Delete Subject
# =====================================

@app.route("/delete_subject/<int:id>")
def delete_subject(id):

    if "user_id" not in session:
        return redirect("/login")

    subject = Subject.query.get_or_404(id)

    db.session.delete(subject)

    db.session.commit()

    flash(
        "Subject Deleted Successfully!",
        "success"
    )

    return redirect("/view_subjects")