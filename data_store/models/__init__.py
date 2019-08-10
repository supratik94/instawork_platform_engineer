__name__ = "Supratik Majumdar"
__status__ = "Development"

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .User import User
