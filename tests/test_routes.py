from werkzeug.exceptions import HTTPException
from app.student_routes import validate_model
from app.models.student import Student
import pytest
import datetime


def test_get_all_students_with_no_records(client):

    response = client.get("/students")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


def test_get_all_students_with_two_records(client, two_saved_students):

    response = client.get("/students")
    response_body = response.get_json()

    assert response.status_code == 200

    print(response_body)
    assert response_body[0] == {
        'date_of_birth': '02/13/1998',
        'email': 'Two@email.com',
        'id': 1,
        'name': 'User Two'
        }
    assert response_body[1] == {
        'date_of_birth': '02/14/1997',
        'email': 'Three@email.com',
        'id': 2,
        'name': 'User Three'}


def test_get_one_student_missing_record(client, two_saved_students):

    response = client.get("/students/3")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Student 3 not found"}


def test_get_one_student_invalid_id(client, two_saved_students):

    response = client.get("/students/hello")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"message": "Student hello invalid"}


def test_get_one_student(client, two_saved_students):

    response = client.get("/students/1")
    response_body = response.get_json()
    print(response_body)

    assert response.status_code == 200
    assert response_body == {
        "Student": {
            'date_of_birth': '02/13/1998',
            'email': 'Two@email.com',
            'id': 1,
            'name': 'User Two'
        }
    }


def test_create_one_student(client):

    response = client.post(
        "/students", json={"name": "New student", "date_of_birth": '01/02/1988', 'email': "email@me.com"}
    )
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == "Student with id '1' successfully created"


def test_create_one_student_no_name(client):

    test_data = {"email": "me@me.com", "date_of_birth": '02/21/1995'}

    with pytest.raises(KeyError, match="name"):
        client.post("/students", json=test_data)

def test_create_one_student_no_dob(client):

    test_data = {"email": "me@me.com", "name": "My name"}

    with pytest.raises(KeyError, match="date_of_birth"):
        client.post("/students", json=test_data)

def test_create_one_student_no_email(client):

    test_data = {"date_of_birth": '02/21/1995', "name": "My name"}

    with pytest.raises(KeyError, match="email"):
        client.post("/students", json=test_data)


def test_validate_model(two_saved_students):

    test_student = validate_model(Student, 1)

    actual = {
        "name": test_student.name,
        "email": test_student.email,
        "date_of_birth": test_student.dob
    }

    expected = {
        'date_of_birth': datetime.date(1998, 2, 13),
        'email': 'Two@email.com',
        'name': 'User Two'
        }

    assert actual == expected


def test_validate_model_missing_record(two_saved_students):
    # Calling `validate_model` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached
    with pytest.raises(HTTPException):
        validate_model(Student, "3")


def test_validate_model_invalid_id(two_saved_students):
    with pytest.raises(HTTPException):
        validate_model(Student, "hello")

