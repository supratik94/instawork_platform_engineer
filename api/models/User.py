__author__ = "Supratik Majumdar"
__status__ = "Development"

from api.models import Base
from sqlalchemy import Column, Integer, String, UniqueConstraint, Enum


class User(Base):
    __tablename__ = "USER"

    id = Column(
        name="ID", type_=Integer, primary_key=True, autoincrement=True, nullable=False
    )
    first_name = Column(name="FIRST_NAME", type_=String(255), nullable=False)
    last_name = Column(name="LAST_NAME", type_=String(255), nullable=False)
    email = Column(name="EMAIL", type_=String(255), nullable=False)
    phone_number = Column(name="PHONE_NUMBER", type_=String(15), nullable=False)
    role = Column(name="ROLE", type_=Enum("ADMIN", "REGULAR"), nullable=False)

    __table_args__ = (
        UniqueConstraint("EMAIL", name="EMAIL_UNIQUE_KEY"),
        UniqueConstraint("PHONE_NUMBER", name="PHONE_NUMBER_UNIQUE_KEY"),
    )
