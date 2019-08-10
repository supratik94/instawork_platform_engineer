__author__ = "Supratik Majumdar"
__status__ = "Development"

from flask_restful import Resource


class User(Resource):
    def get(self):
        return "Hello World"
