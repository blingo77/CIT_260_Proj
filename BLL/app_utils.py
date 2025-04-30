from DAL.models import Student, Faculty, Exams, Location
from DAL.database import db
from flask import current_app
from datetime import datetime

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
        },
    1 :{
        "firstName":"Albert",
        "lastName":"Einstein",
        "email":"albert.einstein@csn.edu",
        "password":"password"
        },
}

location = {
    0:{
        "campus": "henderson"
    },
    1:{
        "campus":"charleston"
    },
    2:{
        "campus":"cheyenne"
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

        for i in range(len(location)):
            new_location = Location(
                campus = location[i]["campus"]
            )

            db.session.add(new_location)
            db.session.commit()

        addExams()


def validateEmail(email):

    #valid emails
    studentEmail = "@student.csn.edu"
    facultyEmail = "@csn.edu"

    atSign = email.find('@')
    emailEnd = email[atSign:].lower()   # splice email to get end
    
    if emailEnd == studentEmail: return 1
    elif emailEnd == facultyEmail: return 2
    else: return 0  #email is not valid

def addExams():
    
    # Step 1: Ensure Faculty and Location exist (or create them)
    faculty = Faculty.query.filter_by(lastName="Coombs").first()
    if not faculty:
        faculty = Faculty(firstName="SomeName", lastName="Coombs", email="coombs@example.com", password="password")
        db.session.add(faculty)
        db.session.commit()

    location = Location.query.filter_by(campus="Henderson").first()
    if not location:
        location = Location(campus="Henderson")
        db.session.add(location)
        db.session.commit()

    # Step 2: Add the exam using the existing Faculty and Location
    new_exam = Exams(
        examName="Fortnite BR",
        examCount=2,
        examCapacity=20,
        examDate=datetime.today().date(),  # or None if not testing this field
        examTime=datetime.now(),  # or None if not testing this field
        facultyId=faculty.id,
        locationId=location.id
    )

    db.session.add(new_exam)
    db.session.commit()

        # Step 1: Ensure Faculty and Location exist (or create them)
    faculty = Faculty.query.filter_by(lastName="Coombs").first()
    if not faculty:
        faculty = Faculty(firstName="SomeName", lastName="Coombs", email="coombs@example.com", password="password")
        db.session.add(faculty)
        db.session.commit()

    location = Location.query.filter_by(campus="Charleston").first()
    if not location:
        location = Location(campus="Charleston")
        db.session.add(location)
        db.session.commit()

    # Step 2: Add the exam using the existing Faculty and Location
    new_exam = Exams(
        examName="Pubg BR",
        examCount=2,
        examCapacity=20,
        examDate=datetime.today().date(),  # or None if not testing this field
        examTime=datetime.now(),  # or None if not testing this field
        facultyId=faculty.id,
        locationId=location.id
    )

    db.session.add(new_exam)
    db.session.commit()