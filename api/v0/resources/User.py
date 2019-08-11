__author__ = "Supratik Majumdar"
__status__ = "Development"

import sqlalchemy
from flask_restful import Resource
from flask_restful import reqparse
from .Resource import API_Resource
from ...models import User as UserSchema
from flask import jsonify, make_response

from ...utilities import validate_mobile_number
from email_validator import validate_email, EmailNotValidError


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

        data = parser.parse_args()
        # Validate email
        try:
            validate_email(
                email=data["e_mail"], check_deliverability=False
            )  # validate and get info
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            return {"message": str(e)}, 400

        # Validate mobile number
        try:
            validate_mobile_number(mobile_number=data["mobile"])
        except ValueError as e:
            return {"message": str(e)}, 400

        # Check First Name and Last name have alteast one character
        if len(data["first_name"]) == 0:
            return {"message": "first_name requires atleast one character"}, 400

        if len(data["last_name"]) == 0:
            return {"message": "last_name requires atleast one character"}, 400

        record = UserSchema(
            first_name=data["first_name"].strip().upper(),
            last_name=data["last_name"].strip().upper(),
            e_mail=data["e_mail"].strip().upper(),
            mobile=data["mobile"].strip(),
            role=data["role"].strip().upper(),
        )

        try:
            self.session.add(record)
            self.session.commit()
            record = (
                self.session.query(UserSchema)
                .filter(UserSchema.mobile == data["mobile"])
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
        except sqlalchemy.exc.IntegrityError as e:
            self.session.rollback()
            error_message = e.args[0]
            if "E_MAIL_UNIQUE_KEY" in error_message:
                return {"message": "e_mail already in use"}, 400

            if "MOBILE_UNIQUE_KEY" in error_message:
                return {"message": "mobile already in use"}, 400

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
