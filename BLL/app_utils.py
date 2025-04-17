from DAL.models import Student, Faculty, Exams
from DAL.database import db
from flask import current_app

students = { 
    0 :{
        "firstName":"Brandon",
        "lastName":"Lingo",
        "email":"brandon.lingo@student.csn.edu",
        "NSHEID":int("5008945170")
        },
    1 :{
        "firstName":"David",
        "lastName":"Pascual",
        "email":"david.pascual@student.csn.edu",
        "NSHEID":int("01")
        },
    2 :{
        "firstName":"Xander",
        "lastName":"Luber-Decena",
        "email":"xander.luber-decena@student.csn.edu",
        "NSHEID":int("0")
        },
    3 :{
        "firstName":"Javier",
        "lastName":"Hernandez",
        "email":"javier.hernandez@student.csn.edu",
        "NSHEID":int("0")
        },
}

faculty = { 
    0 :{
        "firstName":"Karen",
        "lastName":"Coombs",
        "email":"karen.coombs@csn.edu",
        "password":"password"
        }
}

exams = { 
    0 :{
        "examName":"Fortnite BR",
        "examTeacher":"Coombs",
        "examLocation": "Henderson",
        "examCount": 2,
        "examCapacity": 20
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

        for i in range(len(exams)):
            new_exam = Exams(
                examName =  exams[i]["examName"],
                examTeacher  =  exams[i]["examTeacher"],
                examLocation = exams[i]["examLocation"],
                examCount     =  exams[i]["examCount"],
                examCapacity  =  exams[i]["examCapacity"]  # ❗ plain text password – only for testing!
            )

            db.session.add(new_exam)
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
