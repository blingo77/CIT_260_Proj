from flask import Flask, jsonify, request, url_for, flash, redirect, session, render_template
from DAL.database import db, init_database
from DAL.models import User, Student, Faculty, Exams, Location, Report
from .app_utils import createUsers, validateEmail
from datetime import datetime, timedelta, date, time

app = Flask(__name__, template_folder="../presentation/templates", static_folder="../presentation/static")
app.secret_key = "supersecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_database(app=app)
createUsers(app)

@app.context_processor
def inject_logged_in_user():
    return dict(loggedInUser=session.get('user'))

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("NSHEID")

        existing_user = Student.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.")
            return redirect(url_for("signup"))

        new_user = Student(
            firstName=first_name,
            lastName=last_name,
            email=email,
            NSHEID=int(password)
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully!")
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email").lower()
        password = request.form.get("password")

        user_type = validateEmail(email)
        if user_type == 1:
            user = Student.query.filter_by(email=email).first()
            if user and user.NSHEID == int(password):
                session['user'] = {
                    "id": user.id,
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "role": "student"
                }
                return redirect(url_for("confirmation"))
        elif user_type == 2:
            user = Faculty.query.filter_by(email=email).first()
            if user and user.password == password:
                session['user'] = {
                    "id": user.id,
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "role": "faculty"
                }
                return redirect(url_for("confirmation"))

        flash("Invalid login credentials.")
        return redirect(url_for("login"))
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/confirmation')
def confirmation():
    return render_template("confirmation.html")

@app.route('/filter', methods=['GET'])
def filter():
    location = request.args.get('location')
    teacher = request.args.get('teacher')

    query = Exams.query.join(Exams.location).join(Exams.faculty)
    if location:
        query = query.filter(Location.campus == location)
    if teacher:
        query = query.filter(Faculty.lastName == teacher)

    results = query.all()
    faculty_list = Faculty.query.all()
    return render_template("filter.html", exams=results, faculty_list=faculty_list)

@app.route('/exam/<int:exam_id>')
def exam_detail(exam_id):
    exam = Exams.query.get_or_404(exam_id)
    loggedInUser = session.get('user')
    return render_template("exam_detail.html", exam=exam, loggedInUser=loggedInUser, datetime=datetime, timedelta=timedelta)


@app.route('/exam/<int:exam_id>/register', methods=['POST'])
def register_exam(exam_id):
    user = session.get('user')
    if not user or user.get('role') != 'student':
        flash("Only students can register for exams.", "danger")
        return redirect(url_for('exam_detail', exam_id=exam_id))

    student_id = request.form.get('studentId')
    location_id = request.form.get('locationId')
    selected_date = request.form.get('selectedDate')
    selected_time = request.form.get('selectedTime')

    exam = Exams.query.get_or_404(exam_id)
    student = Student.query.get(student_id)

    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for('exam_detail', exam_id=exam_id))

    try:
        date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
        time_obj = datetime.strptime(selected_time, "%H:%M").time()
    except:
        flash("Invalid date/time format.", "danger")
        return redirect(url_for('exam_detail', exam_id=exam_id))

    if Report.query.filter_by(studentId=student.id).count() >= 3:
        flash("You can only register for up to 3 exams.", "warning")
        return redirect(url_for('exam_detail', exam_id=exam_id))

    if Report.query.filter_by(studentId=student.id, examId=exam.id).first():
        flash("You're already registered for this exam.", "warning")
        return redirect(url_for('exam_detail', exam_id=exam_id))

    new_report = Report(
        studentId=student.id,
        examId=exam.id,
        scheduledDate=date_obj,
        scheduledTime=time_obj
    )
    db.session.add(new_report)
    exam.examCount = (exam.examCount or 0) + 1
    db.session.commit()

    flash("Registration successful!", "success")
    return redirect(url_for('exam_detail', exam_id=exam_id))
  

@app.route('/view-exams', methods=['GET'])
def view_exams():
    user = session.get('user')
    if not user or user.get('role') != 'student':
        flash("You must be logged in as a student.")
        return redirect(url_for('login'))

    student_id = user['id']
    exams = db.session.query(Report).join(Exams).filter(
        Report.studentId == student_id
    ).all()
    return render_template('viewExams.html', exams=exams)

@app.route('/cancel-exam', methods=['POST'])
def cancel_exam():
    report_id = request.form.get('exam_registration_id')
    report = Report.query.get(report_id)
    if report:
        db.session.delete(report)
        db.session.commit()
        flash("Exam registration canceled.")
    else:
        flash("Registration not found.")
    return redirect(url_for('view_exams'))

@app.route("/faculty/report")
def faculty_report():
    start_date = request.args.get("start-date")
    end_date = request.args.get("end-date")
    exam_type = request.args.get("exam-type")

    query = Report.query.join(Exams).join(Student).join(Faculty).join(Location)

    if start_date:
        query = query.filter(Exams.examDate >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Exams.examDate <= datetime.strptime(end_date, '%Y-%m-%d').date())
    if exam_type:
        query = query.filter(Exams.examType == exam_type)

    reports = query.all()
    return render_template("faculty/examReport.html", reports=reports)

if __name__ == "__main__":
    app.run(debug=True)
