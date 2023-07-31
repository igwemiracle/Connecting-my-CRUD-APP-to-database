from sqlalchemy import Column, Integer, String, CheckConstraint
from database import Base


class EmployeeData(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150))
    position = Column(String(150))
    job_experience = Column(Integer)
    nationality = Column(String(150))

    __table_args__ = (
        CheckConstraint('job_experience >= 3',
                        name='check_job_experience_min_value'),
    )

    def __repr__(self):
        return '<User %r>' % (self.id)
