from app import db
from datetime import datetime


class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    email = db.Column(db.String, nullable=False)

    @staticmethod
    def convert_date_string(date_string):
        try:
            # parse the date string and return a datetime object
            return datetime.strptime(date_string, "%m/%d/%Y")
        except ValueError:
            # if parsing fails, raise error
            raise ValueError("Invalid date format. Please use MM/DD/YYYY.")

    def to_dict(self):

        dob_date = self.convert_date_string(self.dob) if isinstance(self.dob, str) else self.dob

        student_dict = {
            "id": self.student_id,
            "name": self.name,
            # Convert date back to string
            "date_of_birth": dob_date.strftime("%m/%d/%Y"),
            "email": self.email,
        }

        return student_dict

    @classmethod
    def from_dict(cls, student_data):

        dob_date = cls.convert_date_string(student_data["date_of_birth"])

        new_student = Student(
            name=student_data["name"], dob=dob_date, email=student_data["email"]
        )

        return new_student
