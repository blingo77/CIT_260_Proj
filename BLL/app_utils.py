from DAL.models import User, Student, Faculty
from DAL.database import db
from flask import current_app

students = { 
    0 :{
        "firstName":"Brandon",
        "lastName":"Lingo",
        "email":"brandon.lingo@student.csn.edu",
        "NSHEID":int("5008945170")
        }
}

faculty = { 
    0 :{
        "firstName":"Karen",
        "lastName":"Coombs",
        "email":"karen.coombs@csn.edu",
        "password":"password"
        }
}

def createUsers(app):

    with app.app_context():

        # add students
        for i in range(len(students)):
            new_user = Student(
                firstName =  students[i]["firstName"],
                lastName  =  students[i]["lastName"],
                email     =  students[i]["email"],
                NSHEID    =  students[i]["NSHEID"]  # ❗ plain text password – only for testing!
            )

            db.session.add(new_user)
            db.session.commit()

        # add faculty
        for i in range(len(faculty)):
            new_user = Faculty(
                firstName =  faculty[i]["firstName"],
                lastName  =  faculty[i]["lastName"],
                email     =  faculty[i]["email"],
                password  =  faculty[i]["password"]  # ❗ plain text password – only for testing!
            )

            db.session.add(new_user)
            db.session.commit()

def validateEmail(email):

    #valid emails
    studentEmail = "@student.csn.edu"
    facultyEmail = "@csn.edu"

    atSign = email.find('@')
    emailEnd = email[atSign:].lower()   # splice email to get end
    
    if emailEnd == studentEmail: return 1
    elif emailEnd == facultyEmail: return 2
    else: return 0  #email is not valid
