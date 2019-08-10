__author__ = "Supratik Majumdar"
__status__ = "Development"

import sqlalchemy
from flask_restful import Resource
from flask_restful import reqparse
from .Resource import API_Resource
from ...models import User as UserSchema


class User(API_Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "employee_id",
            help="Employee ID to fetch details for",
            required=False,
            type=int,
            location="args",
        )
        data = parser.parse_args()

        if data["employee_id"] is None:
            employee_list = list()
            records = self.session.query(UserSchema).all()
            for record in records:
                employee_dict = {
                    "employee_id": record.id,
                    "first_name": record.first_name,
                    "last_name": record.last_name,
                    "mobile": record.mobile,
                    "e_mail": record.e_mail,
                    "role": record.role,
                }
                employee_list.append(employee_dict)

            return employee_list
        else:
            try:
                record = (
                    self.session.query(UserSchema)
                    .filter(UserSchema.id == data["employee_id"])
                    .one()
                )
                return {
                    "employee_id": record.id,
                    "first_name": record.first_name,
                    "last_name": record.last_name,
                    "mobile": record.mobile,
                    "e_mail": record.e_mail,
                    "role": record.role,
                }
            except sqlalchemy.orm.exc.NoResultFound:
                return []

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "first_name",
            help="First Name of Employee is mandatory",
            required=True,
            type=str,
            location="json",
        )
        parser.add_argument(
            "last_name",
            help="Last Name of Employee is mandatory",
            required=True,
            type=str,
            location="json",
        )
        parser.add_argument(
            "e_mail",
            help="E-mail of Employee is mandatory",
            required=True,
            type=str,
            location="json",
        )
        parser.add_argument(
            "mobile",
            help="Mobile Number of Employee is mandatory",
            required=True,
            type=str,
            location="json",
        )
        parser.add_argument(
            "role",
            help="Role for Employee is mandatory",
            required=True,
            type=str,
            location="json",
        )
        print(parser.parse_args())

    def patch(self):
        pass

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "employee_id",
            help="Employee ID to fetch details for",
            required=False,
            type=int,
            location="args",
        )
        data = parser.parse_args()
        try:
            record = (
                self.session.query(UserSchema)
                .filter(UserSchema.id == data["employee_id"])
                .one()
            )
            self.session.delete(record)
            self.session.commit()

            return []
        except sqlalchemy.orm.exc.NoResultFound:
            return (
                {"message": f"No record found with employee_id: {data['employee_id']}"},
                400,
            )
