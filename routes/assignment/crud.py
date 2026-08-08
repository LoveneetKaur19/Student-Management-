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
    Subject,
    Assignment
)


# =====================================
# VIEW ASSIGNMENTS
# =====================================

@app.route("/view_assignment")
def view_assignment():

    if "user_id" not in session:
        return redirect("/login")

    assignments = Assignment.query.order_by(
        Assignment.id.desc()
    ).all()

    return render_template(
        "view_assignment.html",
        assignments=assignments,
        today=datetime.today().date()
    )

# =====================================
# ADD ASSIGNMENT
# =====================================

@app.route("/add_assignment", methods=["GET", "POST"])
def add_assignment():

    if "user_id" not in session:
        return redirect("/login")

    subjects = Subject.query.order_by(
        Subject.subject_name
    ).all()

    if request.method == "POST":

        assignment = Assignment(

            title=request.form["title"],

            subject_id=request.form["subject_id"],

            description=request.form["description"],

            due_date=datetime.strptime(
                request.form["due_date"],
                "%Y-%m-%d"
            ).date()

        )

        db.session.add(assignment)

        db.session.commit()

        flash(
            "Assignment Added Successfully!",
            "success"
        )

        return redirect("/view_assignment")

    return render_template(
        "add_assignment.html",
        subjects=subjects
    )

# =====================================
# UPDATE ASSIGNMENT
# =====================================

@app.route("/update_assignment/<int:id>", methods=["GET", "POST"])
def update_assignment(id):

    if "user_id" not in session:
        return redirect("/login")

    assignment = Assignment.query.get_or_404(id)

    subjects = Subject.query.order_by(
        Subject.subject_name
    ).all()

    if request.method == "POST":

        assignment.title = request.form["title"]

        assignment.subject_id = request.form["subject_id"]

        assignment.description = request.form["description"]

        assignment.due_date = datetime.strptime(
            request.form["due_date"],
            "%Y-%m-%d"
        ).date()

        db.session.commit()

        flash(
            "Assignment Updated Successfully!",
            "success"
        )

        return redirect("/view_assignment")

    return render_template(
        "update_assignment.html",
        assignment=assignment,
        subjects=subjects
    )


# =====================================
# DELETE ASSIGNMENT
# =====================================

@app.route("/delete_assignment/<int:id>")
def delete_assignment(id):

    if "user_id" not in session:
        return redirect("/login")

    assignment = Assignment.query.get_or_404(id)

    db.session.delete(assignment)

    db.session.commit()

    flash(
        "Assignment Deleted Successfully!",
        "success"
    )

    return redirect("/view_assignment")