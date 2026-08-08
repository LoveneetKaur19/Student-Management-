from flask import (
    render_template,
    request,
    session,
    redirect
)

from app import app
from models import Students


@app.route("/search_students", methods=["GET", "POST"])
def search_students():

    if "user_id" not in session:
        return redirect("/login")

    students = []

    if request.method == "POST":

        keyword = request.form["keyword"].strip()

        students = Students.query.filter(

            (Students.name.ilike(f"%{keyword}%")) |

            (Students.roll_number.ilike(f"%{keyword}%")) |

            (Students.branch.ilike(f"%{keyword}%")) |

            (Students.semester.ilike(f"%{keyword}%"))

        ).all()

    return render_template(
        "search_students.html",
        students=students
    )