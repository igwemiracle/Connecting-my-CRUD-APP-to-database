from fastapi import FastAPI, status, Request, Depends, Form
import model
from database import engine, sessionLocal
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
model.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = sessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    users = db.query(model.EmployeeData).order_by(model.EmployeeData.id.desc())
    return templates.TemplateResponse("todo.html", {"request": request, "users": users})


@app.post("/add")
async def add(request: Request, name: str = Form(...), position: str = Form(...), job_experience: int = Form(...), nationality: str = Form(...), db: Session = Depends(get_db)):
    users = model.EmployeeData(name=name, position=position,
                               job_experience=job_experience, nationality=nationality)
    db.add(users)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})


@app.get("/edit/{employee_id}")
async def edit(request: Request, employee_id: int, db: Session = Depends(get_db)):
    user = db.query(model.EmployeeData).filter(
        model.EmployeeData.id == employee_id).first()

    return templates.TemplateResponse("edit.html", {"request": request, "user": user})


@app.post("/update/{employee_id}")
async def update(request: Request, employee_id: int, name: str = Form(...), position: str = Form(...), job_experience: int = Form(...), nationality: str = Form(...), db: Session = Depends(get_db)):

    users = db.query(model.EmployeeData).filter(
        model.EmployeeData.id == employee_id).first()

    users.name = name
    users.position = position
    users.job_experience = job_experience
    users.nationality = nationality

    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/delete/{employee_id}")
async def delete(request: Request, employee_id: int, db: Session = Depends(get_db)):
    users = db.query(model.EmployeeData).filter(
        model.EmployeeData.id == employee_id).first()

    db.delete(users)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
