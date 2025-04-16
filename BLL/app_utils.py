from DAL.models import User, Student
from DAL.database import db
from flask import current_app

students = { 
    0 :{
        "firstName":"Brandon",
        "lastName":"Lingo",
        "email":"brandonlingo0@gmail.com",
        "NSHEID":int("5008945170")
        }
}

def createUsers(app):

    with app.app_context():

        for i in range(len(students)):
            new_user = Student(
                firstName =  students[i]["firstName"],
                lastName  =  students[i]["lastName"],
                email     =  students[i]["email"],
                NSHEID    =  students[i]["NSHEID"]  # ❗ plain text password – only for testing!
            )

            db.session.add(new_user)
            db.session.commit()

def validateEmail(email):

    #valid emails
    studentEmail = "@student.csn.edu"
    facultyEmail = "@"

    atSign = email.find('@')
    emailEnd = email[atSign:]   # splice email to get end
    print(emailEnd)