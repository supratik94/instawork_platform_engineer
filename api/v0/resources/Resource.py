__author__ = "Supratik Majumdar"
__status__ = "Development"

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_restful import Resource


class API_Resource(Resource):
    def __init__(self):
        connection_string = (
            "mysql+pymysql://"
            + os.environ["DB_USERNAME"]
            + ":"
            + os.environ["DB_PASSWORD"]
            + "@"
            + os.environ["DB_HOST"]
            + "/"
            + "EMPLOYEE"
        )

        engine = create_engine(connection_string, echo=True)
        session_maker = sessionmaker()
        session_maker.configure(bind=engine)
        self.session = session_maker()
