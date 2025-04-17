from DAL.database import db

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
    examTeacher = db.Column(db.String(100), nullable=False)
    examLocation = db.Column(db.String(100), nullable=False)
    examDate = db.Column(db.Date, nullable=True)
    examTime = db.Column(db.Date, nullable=True)
    examCapacity = db.Column(db.Integer, nullable=True)
    examCount = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return{
            "id": self.id, 
            "ExamName": self.examName, 
            "ExamTeacher": self.examTeacher,
            "ExamDate": self.examDate}
