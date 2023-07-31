from sqlalchemy import Column, Integer, String
from database import Base


class Employee(Base):
    __tablename__ = "employee_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    job_experience = Column(Integer)
    nationality = Column(String)
