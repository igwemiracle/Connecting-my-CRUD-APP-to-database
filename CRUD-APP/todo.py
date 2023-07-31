from fastapi import FastAPI, APIRouter, Path, HTTPException, status, Request, Depends
from pydantic import BaseModel, Field
import model
from database import engine, sessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
model.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = sessionLocal()
        yield db
    finally:
        db.close()


class Employee(BaseModel):
    Name: str = Field(min_length=1)
    Age: int = Field(gt=10)
    JobExperience: int = Field(gt=3, lt=10)
    Nationality: str


todo_list = []


@app.get("/")
async def RetrieveTodos(db: Session = Depends(get_db)):
    return db.query(model.Employee).all()


@app.post("/todo")
async def AddTodo(employee: Employee, db: Session = Depends(get_db)):
    employee_model = model.Employee()
    employee_model.name = employee.Name
    employee_model.age = employee.Age
    employee_model.job_experience = employee.JobExperience
    employee_model.nationality = employee.Nationality

    db.add(employee_model)
    db.commit()
    return employee


@app.put("/todo/{employee_id}")
async def UpdateTodoItem(employee_data: Employee, employee_id: int, db: Session = Depends(get_db)):
    employee_model = db.query(model.Employee).filter(
        model.Employee.id == employee_id).first()
    if employee_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {employee_id}: Does not exist"
        )

    employee_model.name = employee_data.Name
    employee_model.age = employee_data.Age
    employee_model.job_experience = employee_data.JobExperience
    employee_model.nationality = employee_data.Nationality

    db.add(employee_model)
    db.commit()
    return employee_data


@app.delete("/delete/{employee_id}")
async def DeleteSingleTodo(employee_id: int, db: Session = Depends(get_db)):
    employee_model = db.query(model.Employee).filter(
        model.Employee.id == employee_id).first()
    if employee_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo with supplied ID doesn't exist."
        )
    db.query(model.Employee).filter(model.Employee.id == employee_id).delete()
    db.commit()
    return {"Message": f"ID {employee_id} deleted successfully"}
