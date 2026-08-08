import os


class Config:

    SECRET_KEY = "student_management_secret"

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))


    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(
            BASE_DIR,
            "instance",
            "students.db"
        )
    )


    SQLALCHEMY_TRACK_MODIFICATIONS = False


    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "static",
        "uploads"
    )