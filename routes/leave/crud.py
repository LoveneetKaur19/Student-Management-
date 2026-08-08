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
    Leave
)


# =====================================
# VIEW LEAVE
# =====================================

@app.route("/view_leave")
def view_leave():

    if "user_id" not in session:
        return redirect("/login")

    leaves = Leave.query.order_by(
        Leave.id.desc()
    ).all()

    return render_template(
        "view_leave.html",
        leaves=leaves
    )


# =====================================
# ADD LEAVE
# =====================================

@app.route("/add_leave", methods=["GET", "POST"])
def add_leave():

    if "user_id" not in session:
        return redirect("/login")

    students = Students.query.order_by(
        Students.name
    ).all()

    if request.method == "POST":

        leave = Leave(

            student_id=request.form["student_id"],

            from_date=datetime.strptime(
                request.form["from_date"],
                "%Y-%m-%d"
            ).date(),

            to_date=datetime.strptime(
                request.form["to_date"],
                "%Y-%m-%d"
            ).date(),

            reason=request.form["reason"],

            status=request.form["status"]

        )

        db.session.add(leave)

        db.session.commit()

        flash(
            "Leave Added Successfully!",
            "success"
        )

        return redirect("/view_leave")

    return render_template(
        "add_leave.html",
        students=students
    )


# =====================================
# UPDATE LEAVE
# =====================================

@app.route("/update_leave/<int:id>", methods=["GET", "POST"])
def update_leave(id):

    if "user_id" not in session:
        return redirect("/login")

    leave = Leave.query.get_or_404(id)

    students = Students.query.order_by(
        Students.name
    ).all()

    if request.method == "POST":

        leave.student_id = request.form["student_id"]

        leave.from_date = datetime.strptime(
            request.form["from_date"],
            "%Y-%m-%d"
        ).date()

        leave.to_date = datetime.strptime(
            request.form["to_date"],
            "%Y-%m-%d"
        ).date()

        leave.reason = request.form["reason"]

        leave.status = request.form["status"]

        db.session.commit()

        flash(
            "Leave Updated Successfully!",
            "success"
        )

        return redirect("/view_leave")

    return render_template(
        "update_leave.html",
        leave=leave,
        students=students
    )


# =====================================
# DELETE LEAVE
# =====================================

@app.route("/delete_leave/<int:id>")
def delete_leave(id):

    if "user_id" not in session:
        return redirect("/login")

    leave = Leave.query.get_or_404(id)

    db.session.delete(leave)

    db.session.commit()

    flash(
        "Leave Deleted Successfully!",
        "success"
    )

    return redirect("/view_leave")