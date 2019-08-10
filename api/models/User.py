__author__ = "Supratik Majumdar"
__status__ = "Development"

from api.models import Base
from sqlalchemy import Column, Integer, String, UniqueConstraint


class User(Base):
    __tablename__ = "USER"

    id = Column(
        name="ID", type_=Integer, primary_key=True, autoincrement=True, nullable=False
    )
    first_name = Column(name="FIRST_NAME", type_=String(255), nullable=False)
    last_name = Column(name="LAST_NAME", type_=String(255), nullable=False)
    e_mail = Column(name="E_MAIL", type_=String(255), nullable=False)
    mobile = Column(name="MOBILE", type_=String(15), nullable=False)
    role = Column(name="ROLE", type_=String(10), nullable=False)

    __table_args__ = (
        UniqueConstraint("E_MAIL", name="E_MAIL_UNIQUE_KEY"),
        UniqueConstraint("MOBILE", name="MOBILE_UNIQUE_KEY"),
    )
