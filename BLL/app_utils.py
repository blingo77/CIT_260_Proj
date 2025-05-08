from DAL.models import Student, Faculty, Exams, Location
from DAL.database import db
from flask import current_app
from datetime import datetime

students = {
    0: {
        "firstName": "Brandon",
        "lastName": "Lingo",
        "email": "brandon.lingo@student.csn.edu",
        "NSHEID": int("5008945170")
    },
    1: {
        "firstName": "David",
        "lastName": "Pascual",
        "email": "david.pascual@student.csn.edu",
        "NSHEID": int("01")
    },
    2: {
        "firstName": "Xander",
        "lastName": "Luber-Decena",
        "email": "xander.luber-decena@student.csn.edu",
        "NSHEID": int("0")
    },
    3: {
        "firstName": "Javier",
        "lastName": "Hernandez",
        "email": "javier.hernandez@student.csn.edu",
        "NSHEID": int("0")
    },
}

faculty = {
    0: {
        "firstName": "Karen",
        "lastName": "Coombs",
        "email": "karen.coombs@csn.edu",
        "password": "password"
    },
    1: {
        "firstName": "Albert",
        "lastName": "Einstein",
        "email": "albert.einstein@csn.edu",
        "password": "password"
    },
}

location = {
    0: {"campus": "henderson"},
    1: {"campus": "West Charleston"},
    2: {"campus": "cheyenne"}
}


def createUsers(app):
    with app.app_context():
        for i in range(len(students)):
            new_user = Student(
                firstName=students[i]["firstName"],
                lastName=students[i]["lastName"],
                email=students[i]["email"],
                NSHEID=students[i]["NSHEID"]
            )
            db.session.add(new_user)
            db.session.commit()

        for i in range(len(faculty)):
            new_user = Faculty(
                firstName=faculty[i]["firstName"],
                lastName=faculty[i]["lastName"],
                email=faculty[i]["email"],
                password=faculty[i]["password"]
            )
            db.session.add(new_user)
            db.session.commit()

        for i in range(len(location)):
            new_location = Location(campus=location[i]["campus"])
            db.session.add(new_location)
            db.session.commit()

        addExams()


def validateEmail(email):
    studentEmail = "@student.csn.edu"
    facultyEmail = "@csn.edu"
    atSign = email.find('@')
    emailEnd = email[atSign:].lower()

    if emailEnd == studentEmail:
        return 1
    elif emailEnd == facultyEmail:
        return 2
    else:
        return 0


def addExams():
    def ensure_faculty_and_location(campus):
        faculty = Faculty.query.filter_by(lastName="Coombs").first()
        if not faculty:
            faculty = Faculty(firstName="Karen", lastName="Coombs", email="coombs@example.com", password="password")
            db.session.add(faculty)
            db.session.commit()

        location = Location.query.filter_by(campus=campus).first()
        if not location:
            location = Location(campus=campus)
            db.session.add(location)
            db.session.commit()

        return faculty, location

    exams = [
        ("Introduction to Fortnite FTNT101", "Henderson", 2, 20, "quiz"),
        ("PUBG Tactics PUBG202", "West Charleston", 2, 20, "midterm"),
        ("Apex Legends Third Party Logic APL114", "Cheyenne", 0, 20, "quiz"),
        ("Rocket League History RTL210", "West Charleston", 0, 20, "quiz"),
        ("Halo Media Ethics HLO203", "Henderson", 0, 20, "final"),
        ("Call of Duty Zombies Stratigical Analysis COD208", "Cheyenne", 20, 20, "final")
    ]


    for examName, campus, examCount, examCapacity, examType in exams:
        faculty, location = ensure_faculty_and_location(campus)
        new_exam = Exams(
            examName=examName,
            examCount=examCount,
            examCapacity=examCapacity,
            examType=examType,
            examDate=datetime.today().date(),
            examTime=datetime.now(),
            facultyId=faculty.id,
            locationId=location.id
        )
        db.session.add(new_exam)
        db.session.commit()

