__author__ = "Supratik Majumdar"
__status__ = "Development"

import os
from sqlalchemy import create_engine
from api.models import Base
from sqlalchemy_utils import create_database, database_exists

if __name__ == "__main__":
    connection_string = (
        "mysql+pymysql://"
        + os.environ["ROOT_DB_USERNAME"]
        + ":"
        + os.environ["ROOT_DB_PASSWORD"]
        + "@"
        + os.environ["DB_HOST"]
        + "/"
        + "EMPLOYEE"
    )

    if not database_exists(connection_string):
        create_database(connection_string)

    engine = create_engine(connection_string, echo=True)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine, checkfirst=True)
