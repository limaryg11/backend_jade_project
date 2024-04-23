from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.student import Student

student_bp = Blueprint("student_bp", __name__, url_prefix="/students")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except Exception as error:
        print(error)
        # 400 = bad request
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    # this method queries database for instance of model class with given id
    model = cls.query.get(model_id)

    if not model:
        # 404 = Not Found
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model


@student_bp.route("", methods=["POST"])
def create_student():
    request_body = request.get_json()

    new_student = Student.from_dict(request_body)

    db.session.add(new_student)

    db.session.commit()

    return (
        jsonify(f"Student with id '{new_student.student_id}' successfully created"),
        201,
    )


@student_bp.route("", methods=["GET"])
def get_all_students():

    students = Student.query.all()

    response = [student.to_dict() for student in students]

    return jsonify(response), 200


@student_bp.route("/<student_id>", methods=["GET"])
def get_student_by_id(student_id):

    student = validate_model(Student, student_id)

    return jsonify({"Student": student.to_dict()}), 200


@student_bp.route("/<student_id>", methods=["PUT"])
def update_student(student_id):
    student = validate_model(Student, student_id)

    request_data = request.get_json()

    student.name = request_data["name"]
    student.dob = request_data["date_of_birth"]
    student.email = request_data["email"]

    db.session.commit()

    return (
        jsonify(
            {"message": f"Student with id {student.student_id} successfully updated"}
        ),
        200,
    )


@student_bp.route("/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = validate_model(Student, student_id)

    db.session.delete(student)

    db.session.commit()

    return (
        jsonify(
            {"message": f"Student with id {student.student_id} successfully deleted"}
        ),
        200,
    )
