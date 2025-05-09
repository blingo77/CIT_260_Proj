from DAL.database import db
from datetime import date, time
from sqlalchemy import Date, Time

class User(db.Model):
    __tablename__ = 'users'  # Optional, sets table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}
    
class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    NSHEID = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return{
            "id": self.id, 
            "FirstName": self.firstName, 
            "LastName": self.lastName,
            "Email": self.email,
            "NSHEID": self.NSHEID}
    
class Faculty(db.Model):
    __tablename__ = "faculty"
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return{
            "id": self.id, 
            "FirstName": self.firstName, 
            "LastName": self.lastName,
            "password": self.password,
            "Email": self.email}

class Exams(db.Model):
    __tablename__ = "exams"
    id = db.Column(db.Integer, primary_key=True)
    examName = db.Column(db.String(100), nullable=False)
    examDate = db.Column(db.Date, nullable=True)
    examTime = db.Column(db.Date, nullable=True)
    examType = db.Column(db.String(20), nullable=False, default="quiz")
    examCapacity = db.Column(db.Integer, nullable=True)
    examCount = db.Column(db.Integer, nullable=True)

    facultyId = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=True)
    locationId = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)

    faculty = db.relationship('Faculty', backref='exams', lazy=True)
    location = db.relationship('Location', backref='exams', lazy=True)

    def to_dict(self):
        return{
            "id": self.id, 
            "ExamName": self.examName, 
            "ExamTeacher": self.examTeacher,
            "ExamDate": self.examDate}

class Location(db.Model):
    __tablename = "location"
    id = db.Column(db.Integer, primary_key=True)
    campus = db.Column(db.String(100), nullable=False)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('students.id'))
    examId = db.Column(db.Integer, db.ForeignKey('exams.id'))
    
    # NEW FIELDS
    scheduledDate = db.Column(Date)
    scheduledTime = db.Column(Time)

    student = db.relationship('Student', backref='reports')
    exam = db.relationship('Exams', backref='reports')