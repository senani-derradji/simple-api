from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import User
from sqlalchemy.orm import sessionmaker
from db import engine
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.responses import FileResponse

session_local = sessionmaker(bind=engine, autocommit=False, autoflush=False)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class STUDENT(BaseModel):
    name: str
    age: int
    grade: str

@app.get("/", include_in_schema=False)
def serve_index():
    file_path = Path(__file__).parent / "index.html"
    return FileResponse(file_path)


@app.get("/students/")
def get_students():
    session = session_local()
    students = session.query(User).all()
    session.close()
    return {"students": students}


@app.post("/students/")
def add_student(student: STUDENT):
    session = session_local()
    new_student = User(name=student.name, age=student.age, grade=student.grade)
    session.add(new_student)
    session.commit()
    session.close()
    return {"message": f"{new_student.name} added successfully"}

@app.put("/students/{student_id}")
def update_student(student_id: int, student: STUDENT):
    session = session_local()
    db_student = session.query(User).filter(User.id == student_id).first()
    if not db_student:
        session.close()
        raise HTTPException(status_code=404, detail=f"Student {db_student} not found")
    db_student.name = student.name
    db_student.age = student.age
    db_student.grade = student.grade
    session.commit()
    session.close()
    return {"message": "Student {db_student.name} has been updated successfully"}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    session = session_local()
    db_student = session.query(User).filter(User.id == student_id).first()
    if not db_student:
        session.close()
        raise HTTPException(status_code=404, detail=f"Student {db_student} not found")
    session.delete(db_student)
    session.commit()
    session.close()
    return {"message": f"Student {db_student.name} has been deleted successfully"}
