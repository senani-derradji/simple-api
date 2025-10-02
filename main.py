from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

students = [
        {"name": "Alice", "age": 20, "grade": "A", "city": "New York"},
        {"name": "Bob", "age": 22, "grade": "B", "city": "Los Angeles"},
        {"name": "Charlie", "age": 23, "grade": "C", "city": "Chicago"},
        {"name": "David", "age": 21, "grade": "B", "city": "Houston"},
        {"name": "Eva", "age": 24, "grade": "A", "city": "Phoenix"},]

class STUDENT(BaseModel):
    name: str
    age: int
    grade: str
    city: str

@app.get("/students/")
def get_students():
    return students

@app.post("/students/")
def add_student(student: STUDENT):
    students.append(student)
    return {"message": "Student added successfully"}

@app.put("/students/{age}")
def update_student(s_name: str, student: STUDENT):
    for s in students:
        if s['name'] == s_name:
            s.update(student.dict())
            return {"message": "Student updated successfully"}
    return {"message": "Student not found"}

@app.delete("/students/{age}")
def delete_student(std_age: int):
    for s in students:
        if s["age"] == std_age:
            students.remove(s)
            return {"message": "Student has been deleted"}
    return {"error": "This student not found !!"}