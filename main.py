from fastapi import FastAPI, Path
from schemas.student import Student
from config.db import con
from models.index import students

app=FastAPI()

# Get All Students from the DB
@app.get('/api/students')
async def get_all_students():
    data=con.execute(students.select()).fetchall()
    return {
        "students":data
    }

# Get student by ID
@app.get('/api/students/{id}')
async def get_student_by_id(id:int = Path(title="Please insert a valid student ID",ge=1)):
    data=con.execute(students.select().where(students.c.id==id)).fetchall()
    return {
        "students":data
    }

# Add a student
@app.post('/api/students')
async def add_student(student:Student):
    data=con.execute(students.insert().values(
        name=student.name,
        email=student.email
    ))

    if data.is_insert:
        # is_insert is a ORM state which returns True if this is an INSERT operation.
        # from here, I used data.lastrowid, which is the latest ID generated, to fetcb that new student
        # So that the API can return the latest student added
        # I cannot find another way (there should be!) to do in smarter
        
        newdata=con.execute(students.select().where(students.c.id==data.lastrowid)).fetchall()
        return {
            "students":newdata
        }
    else:
         return {
            "msg":"An error occured when adding a student"
        }

# edit data
@app.patch('/api/students/{id}')
async def edit_data(id:int):
    data=con.execute(students.select().where(students.c.id==id)).fetchall()
    return {
        "success": True,
        "data":data
    }

# update data

@app.put('/api/students/{id}')
async def update(id:int,student:Student):
    data=con.execute(students.update().values(
        name=student.name,
        email=student.email,
    ).where(students.c.id==id))
    if data:
        return {
            "success": True,
            "msg":"Student Update Successfully"
        }
    else:
         return {
            "success": False,
            "msg":"Some Problem"
        }

# delete data
@app.delete('/api/students/{id}')
async def delete(id:int):
    data=con.execute(students.delete().where(students.c.id==id))
    if data:
        return {
            "success": True,
            "msg":"Student Delete Successfully"
        }
    else:
         return {
            "success": False,
            "msg":"Some Problem"
        }

# search data

@app.get('/api/students/{search}')
async def search(search):
    data=con.execute(students.select().where(students.c.name.like('%'+search+'%'))).fetchall()
    return {
        "success": True,
        "data":data
    }