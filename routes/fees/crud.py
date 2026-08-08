from flask import (
    render_template,
    request,
    redirect,
    session,
    flash
)

from datetime import datetime
from sqlalchemy import func

from app import app

from models import (
    db,
    Students,
    FeePayment
)


# =====================================
# UPDATE STUDENT FEE DETAILS
# =====================================

def update_student_fee(student_id):

    student = Students.query.get(student_id)

    if not student:
        return

    total_paid = db.session.query(
        func.sum(FeePayment.amount)
    ).filter(
        FeePayment.student_id == student_id
    ).scalar()

    if total_paid is None:
        total_paid = 0

    student.paid_fee = total_paid

    student.due_fee = (
        student.total_fee -
        student.paid_fee
    )

    if student.due_fee <= 0:

        student.due_fee = 0

        student.fee_status = "Paid"

    else:

        student.fee_status = "Pending"


# =====================================
# ADD FEE
# =====================================

@app.route("/add_fee", methods=["GET", "POST"])
def add_fee():

    if "user_id" not in session:
        return redirect("/login")

    students = Students.query.order_by(
        Students.name
    ).all()

    if request.method == "POST":

        student_id = int(
            request.form["student_id"]
        )

        amount = float(
            request.form["amount"]
        )

        payment_mode = request.form[
            "payment_mode"
        ]

        receipt_number = request.form[
            "receipt_number"
        ].strip()

        student = Students.query.get_or_404(
            student_id
        )

        # ----------------------------
        # Amount Validation
        # ----------------------------

        if amount <= 0:

            flash(
                "Amount must be greater than zero.",
                "danger"
            )

            return redirect("/add_fee")

        # ----------------------------
        # Duplicate Receipt Validation
        # ----------------------------

        receipt = FeePayment.query.filter_by(
            receipt_number=receipt_number
        ).first()

        if receipt:

            flash(
                "Receipt Number Already Exists.",
                "danger"
            )

            return redirect("/add_fee")

        # ----------------------------
        # Over Payment Validation
        # ----------------------------

        if amount > student.due_fee:

            flash(
                "Payment exceeds remaining Due Fee.",
                "danger"
            )

            return redirect("/add_fee")

        payment = FeePayment(

            student_id=student_id,

            amount=amount,

            payment_mode=payment_mode,

            receipt_number=receipt_number,

            payment_date=datetime.today().date()

        )

        db.session.add(payment)

        db.session.flush()

        update_student_fee(student_id)

        db.session.commit()

        flash(
            "Fee Payment Added Successfully!",
            "success"
        )

        return redirect("/fee_history")

    return render_template(

        "add_fee.html",

        students=students

    )


# =====================================
# VIEW FEE HISTORY
# =====================================

@app.route("/fee_history")
def fee_history():

    if "user_id" not in session:
        return redirect("/login")

    payments = FeePayment.query.order_by(
        FeePayment.payment_date.desc()
    ).all()

    return render_template(
        "fee_history.html",
        payments=payments
    )


# =====================================
# UPDATE FEE
# =====================================

@app.route("/update_fee/<int:id>", methods=["GET", "POST"])
def update_fee(id):

    if "user_id" not in session:
        return redirect("/login")

    payment = FeePayment.query.get_or_404(id)

    students = Students.query.order_by(
        Students.name
    ).all()

    if request.method == "POST":

        old_student_id = payment.student_id

        new_student_id = int(
            request.form["student_id"]
        )

        amount = float(
            request.form["amount"]
        )

        payment_mode = request.form[
            "payment_mode"
        ]

        receipt_number = request.form[
            "receipt_number"
        ].strip()

        # ----------------------------
        # Amount Validation
        # ----------------------------

        if amount <= 0:

            flash(
                "Amount must be greater than zero.",
                "danger"
            )

            return redirect(f"/update_fee/{id}")

        # ----------------------------
        # Receipt Validation
        # ----------------------------

        receipt = FeePayment.query.filter(
            FeePayment.receipt_number == receipt_number,
            FeePayment.id != payment.id
        ).first()

        if receipt:

            flash(
                "Receipt Number Already Exists.",
                "danger"
            )

            return redirect(f"/update_fee/{id}")

        student = Students.query.get_or_404(
            new_student_id
        )

        # ----------------------------
        # Calculate Already Paid
        # ----------------------------

        if old_student_id == new_student_id:

            already_paid = db.session.query(
                func.sum(FeePayment.amount)
            ).filter(
                FeePayment.student_id == new_student_id,
                FeePayment.id != payment.id
            ).scalar()

        else:

            already_paid = db.session.query(
                func.sum(FeePayment.amount)
            ).filter(
                FeePayment.student_id == new_student_id
            ).scalar()

        if already_paid is None:
            already_paid = 0

        remaining_fee = (
            student.total_fee -
            already_paid
        )

        if amount > remaining_fee:

            flash(
                "Payment exceeds remaining Due Fee.",
                "danger"
            )

            return redirect(f"/update_fee/{id}")

        # ----------------------------
        # Update Payment
        # ----------------------------

        payment.student_id = new_student_id

        payment.amount = amount

        payment.payment_mode = payment_mode

        payment.receipt_number = receipt_number

        db.session.flush()

        update_student_fee(
            old_student_id
        )

        update_student_fee(
            new_student_id
        )

        db.session.commit()

        flash(
            "Fee Updated Successfully!",
            "success"
        )

        return redirect("/fee_history")

    return render_template(

        "update_fee.html",

        payment=payment,

        students=students

    )


# =====================================
# DELETE FEE
# =====================================

@app.route("/delete_fee/<int:id>")
def delete_fee(id):

    if "user_id" not in session:
        return redirect("/login")

    payment = FeePayment.query.get_or_404(id)

    student_id = payment.student_id

    db.session.delete(payment)

    db.session.flush()

    update_student_fee(student_id)

    db.session.commit()

    flash(
        "Fee Payment Deleted Successfully!",
        "success"
    )

    return redirect("/fee_history")


# =====================================
# FEE DEFAULTERS
# =====================================

@app.route("/fee_defaulters")
def fee_defaulters():

    if "user_id" not in session:
        return redirect("/login")

    students = Students.query.filter(
        Students.due_fee > 0
    ).order_by(
        Students.due_fee.desc()
    ).all()

    return render_template(
        "fee_defaulters.html",
        students=students
    )