from flask import Flask, render_template
from config import Config
from models import db

app = Flask(__name__)

# ----------------------------
# Load Configuration
# ----------------------------

app.config.from_object(Config)

# ----------------------------
# Initialize Database
# ----------------------------

db.init_app(app)


#Importing routes
import routes.auth
import routes.dashboard

import routes.students.crud
import routes.students.search
import routes.students.profile

import routes.subjects.crud

import routes.enrollments.crud
import routes.attendance.crud
import routes.marks.crud
import routes.fees.crud
import routes.assignment.crud
import routes.leave.crud


#temporary test route
@app.route("/test")
def test():
    return "TEST OK"



# ----------------------------
# Create Database
# ----------------------------

with app.app_context():
    db.create_all()


# ==========================================================
# ERROR HANDLERS
# ==========================================================

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500


# ==========================================================
# RUN APP
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True)

