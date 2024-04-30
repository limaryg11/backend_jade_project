import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from pathlib import Path
from app.models.student import Student
import pandas as pd


# this fixture sets up a Flask app instance for testing
@pytest.fixture
def app():
    # create flask app instance for testing
    app = create_app({"TESTING": True})

    # this decorator essentially says when a request finishes processing the flask
    # app, then execute this function
    @request_finished.connect_via(app)
    # signal handler registered to disconnect db session when request is finished
    def expire_session(sender, response, **extra):
        db.session.remove()

    # creates all the database tables and yields app instance for tests
    with app.app_context():
        db.create_all()
        yield app

    # after tests run, drops all the database tables
    with app.app_context():
        db.drop_all()


# fixture to provide test client for interacting with flask app
@pytest.fixture
def client(app):
    return app.test_client()


# get file path fixture for test_data
@pytest.fixture()
def get_file():
    def _(file_path: str):
        return Path(__file__).parent / f"data/{file_path}"

    return _


# fixture to read data from csv test data and add in as objects to data arr
@pytest.fixture
def student_data_from_csv(get_file):
    data = []
    file_name = get_file("sample_data.csv")
    customer_data = pd.read_csv(file_name)

    for index, row in customer_data.iterrows():

        row_data = {
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "date_of_birth": row["dob"],
        }
        data.append(row_data)

    return data


@pytest.fixture
def two_saved_students(app, student_data_from_csv):
    student_1  = student_data_from_csv[1]
    student_1_from = Student.from_dict(student_1)

    student_2  = student_data_from_csv[2]
    student_2_from = Student.from_dict(student_2)

    db.session.add_all([student_1_from, student_2_from])
    db.session.commit()
