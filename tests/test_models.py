from app.models.student import Student

import pytest


def test_student_from_dict_to_dict(student_data_from_csv):

    actual = []
    expected = []

    # testing to/from dict methods for Student model
    for actual_row in student_data_from_csv:
        student_object = Student.from_dict(actual_row)
        student_dict = student_object.to_dict()
        actual_data = {
            "name": student_dict["name"],
            "email": student_dict["email"],
            "date_of_birth": student_dict["date_of_birth"],
        }
        actual.append(actual_data)

    for row2 in student_data_from_csv:

        row2_data = {
            "name": row2["name"],
            "email": row2["email"],
            "date_of_birth": row2["date_of_birth"],
        }
        expected.append(row2_data)

    assert actual == expected


def test_student_to_dict_no_missing_data(student_data_from_csv):
    expected = student_data_from_csv[1]

    test_data = Student(
        student_id=expected["id"],
        name=expected["name"],
        email=expected["email"],
        dob=expected["date_of_birth"],
    )
    actual = test_data.to_dict()

    assert actual == expected


def test_student_to_dict_missing_id(student_data_from_csv):

    mock_data = student_data_from_csv[1]

    test_data = Student(
        name=mock_data["name"], email=mock_data["email"], dob=mock_data["date_of_birth"]
    )

    result = test_data.to_dict()

    assert result["id"] is None
    assert result["name"] == mock_data["name"]
    assert result["email"] == mock_data["email"]
    assert result["date_of_birth"] == mock_data["date_of_birth"]


def test_to_dict_missing_other__dob(student_data_from_csv):

    mock_data = student_data_from_csv[1]

    test_data = Student(student_id=mock_data["id"])

    with pytest.raises(AttributeError):
        test_data.to_dict()


def test_to_dict_missing_other__vals(student_data_from_csv):

    mock_data = student_data_from_csv[1]

    test_data = Student(student_id=mock_data["id"], dob=mock_data["date_of_birth"])

    result = test_data.to_dict()

    assert result["id"] == mock_data["id"]
    assert result["name"] is None
    assert result["email"] is None


def test_student_from_dict_returns_student(student_data_from_csv):
    mock_data = student_data_from_csv[1]

    student = Student.from_dict(mock_data)

    actual = {
        "name": student.name,
        "date_of_birth": student.dob,
        "email": student.email,
    }

    expected = {
        "name": mock_data["name"],
        "date_of_birth": Student.convert_date_string(mock_data["date_of_birth"]),
        "email": mock_data["email"],
    }

    assert actual == expected


def test_student_from_dict_missing_email():
    mock_data = {"name": "Ada Lovelace", "date_of_birth": "02/14/1997"}

    with pytest.raises(KeyError, match="email"):
        Student.from_dict(mock_data)


def test_student_from_dict_missing_dob():
    mock_data = {"name": "Ada Lovelace", "email": "me@me.com"}

    with pytest.raises(KeyError, match="date_of_birth"):
        Student.from_dict(mock_data)


def test_student_from_dict_missing_name():
    mock_data = {"date_of_birth": "02/13/1997", "email": "me@me.com"}

    with pytest.raises(KeyError, match="name"):
        Student.from_dict(mock_data)
