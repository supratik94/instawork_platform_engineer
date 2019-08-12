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
                    "phone_number": record.phone_number,
                    "email": record.email,
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
                    "phone_number": record.phone_number,
                    "email": record.email,
                    "role": record.role,
                }
            except sqlalchemy.orm.exc.NoResultFound:
                return []

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "first_name",
            help="first_name of Employee is mandatory",
            required=True,
            type=str,
            location="json",
        )
        parser.add_argument(
            "last_name",
            help="last_name of Employee is mandatory",
            required=True,
            type=str,
            location="json",
        )
        parser.add_argument(
            "email",
            help="email of Employee is mandatory",
            required=True,
            type=str,
            location="json",
        )
        parser.add_argument(
            "phone_number",
            help="phone_number of Employee is mandatory",
            required=True,
            type=str,
            location="json",
        )
        parser.add_argument(
            "role",
            help="Role for Employee can only be admin or regualar",
            required=True,
            type=str,
            location="json",
            choices=("admin", "regular"),
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
        if len(data["first_name"].strip()) == 0:
            return {"message": "first_name requires atleast one character"}, 400

        if len(data["last_name"].strip()) == 0:
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
            return (
                {
                    "employee_id": record.id,
                    "first_name": record.first_name,
                    "last_name": record.last_name,
                    "phone_number": record.phone_number,
                    "email": record.email,
                    "role": record.role,
                },
                201,
            )
        except sqlalchemy.exc.IntegrityError as e:
            self.session.rollback()
            error_message = e.args[0]
            if "EMAIL_UNIQUE_KEY" in error_message:
                return {"message": "email already in use"}, 400

            if "PHONE_NUMBER_UNIQUE_KEY" in error_message:
                return {"message": "phone_number already in use"}, 400

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "employee_id",
            help="employee_id to update details for",
            required=True,
            type=int,
            location="args",
        )
        parser.add_argument(
            "first_name",
            help="first_name of Employee",
            required=False,
            type=str,
            location="json",
        )
        parser.add_argument(
            "last_name",
            help="last_name of Employee",
            required=False,
            type=str,
            location="json",
        )
        parser.add_argument(
            "email", help="email of Employee", required=True, type=str, location="json"
        )
        parser.add_argument(
            "phone_number",
            help="phone_number of Employee",
            required=False,
            type=str,
            location="json",
        )
        parser.add_argument(
            "role",
            help="Role for Employee can only be admin or regualar",
            required=False,
            type=str,
            location="json",
            choices=("admin", "regular"),
        )
        data = parser.parse_args()
        update_dict = dict()

        for key, value in data.items():
            if key != "employee_id":
                if value is not None:
                    update_dict[key] = data[key]

        if len(update_dict) == 0:
            return (
                {"message": "Nothing to update, pass at least one field to update"},
                400,
            )

        else:
            try:
                # Fetch to check if employee_id exists
                record = (
                    self.session.query(UserSchema)
                    .filter(UserSchema.id == data["employee_id"])
                    .one()
                )

                # Update Record
                self.session.query(UserSchema).filter(
                    UserSchema.id == data["employee_id"]
                ).update(update_dict)
                self.session.commit()

                # Fetch Updated record and return
                record = (
                    self.session.query(UserSchema)
                    .filter(UserSchema.id == data["employee_id"])
                    .one()
                )
                return {
                    "employee_id": record.id,
                    "first_name": record.first_name,
                    "last_name": record.last_name,
                    "phone_number": record.phone_number,
                    "email": record.email,
                    "role": record.role,
                }

            except sqlalchemy.orm.exc.NoResultFound:
                return (
                    {
                        "message": f"No record found with employee_id: {data['employee_id']}"
                    },
                    400,
                )

            except sqlalchemy.exc.IntegrityError as e:
                self.session.rollback()
                error_message = e.args[0]
                if "EMAIL_UNIQUE_KEY" in error_message:
                    return {"message": "email already in use"}, 400

                if "PHONE_NUMBER_UNIQUE_KEY" in error_message:
                    return {"message": "phone_number already in use"}, 400

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "employee_id",
            help="Employee ID to delete data for",
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

            return [], 204
        except sqlalchemy.orm.exc.NoResultFound:
            return (
                {"message": f"No record found with employee_id: {data['employee_id']}"},
                400,
            )
