from database import Base
from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, nullable=False, primary_key=True)
    first_name = Column(String, nullable=False)
    last_surname = Column(String, nullable=False)
    city = Column(String, nullable=False)
    roles = Column(String, nullable=False)



SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost:5433/inka_company'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)
