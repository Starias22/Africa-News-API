# import fastapi

# Our first API
from fastapi import FastAPI,Path
students={
1:{
        "name":"John",
        "age":17,
        "year":"year 12"
}
}
app=FastAPI()

# / as endpoint; it is the homepage
@app.get("/")
# Name it index or home
def index():
        return {"name":"First data"}

"""@app.get("/get-student/{student_id}")
def get_student(student_id:int):
        return students[student_id]
"""
# ... means required and even when not specified, the param is required
"""@app.get("/get-student/{student_id}")
def get_student(student_id:int=Path(...,description="The ID of the student you want to view")):
        return students[student_id]"""

@app.get("/get-student/{student_id}")
def get_student(student_id:int=Path(...,description="The ID of the student you want to view. Must be greatr than 0",gt=0,le=3)):
        return students[student_id]

"""@app.get("/get-by-name")
def get_student(name:str): # set it to None to make it not required or use name:Optional[str]=None where Optional is imported from typing
        for student_id in students:
                if students[student_id]["name"]==name:
                        return students[student_id]
        return {"Data":"Not found"}"""

# Using multiple query params


# an error so 
#def get_student(name:str=None,test:int): # set it to None to make it not required or use name:Optional[str]=None where Optional is imported from typing
 
# first way
@app.get("/get-by-name")
def get_student(test:int,name:str=None):
        for student_id in students:
                if students[student_id]["name"]==name:
                        return students[student_id]
        return {"Data":"Not found"}

# second way way
"""@app.get("/get-by-name")
def get_student(*,name:str=None,test:int):
        for student_id in students:
                if students[student_id]["name"]==name:
                        return students[student_id]
        return {"Data":"Not found"}"""

# Combining
@app.get("/get-by-name/{student_id}")
def get_student(*,student_id,name:str=None,test:int):
        for student_id in students:
                if students[student_id]["name"]==name:
                        return students[student_id]
        return {"Data":"Not found"}

from pydantic import BaseModel
class Student(BaseModel):
        name:str
        age:int
        year:str

@app.post("/create-student/{student_id}")
def create_student(student_id:int,student:Student):
        if student_id in students:
                return {"Error:","Student already exixts"}
        students[student_id]=student
        return students[student_id]

from typing import Optional
class UpdateStudent(BaseModel):
        name:Optional[str]=None
        age:Optional[int]=None
        year:Optional[str]=None



@app.put("/update-student/{student_id}")
def update_student(student_id:int,student:UpdateStudent):
        if student_id not in students:
                return {"Error:","That student dos not exist"}
        students[student_id]=student
        if student.name!=None:
                students[student_id].name=student.name

        if student.age!=None:
                students[student_id].age=student.age
        if student.year!=None:
                students[student_id].year=student.year
        return students[student_id]

@app.delete("/delete-delete/{student_id}")
def delete_student(student_id:int):
        if student_id not in students:
                return {"Error:","That student does not exist"}
        
        del students[student_id]
        return {"Sucess:":"Student deleted"}
