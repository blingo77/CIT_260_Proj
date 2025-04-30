from flask import Flask, jsonify, request, url_for, flash, redirect, session
from flask import render_template
from DAL.database import db, init_database
from DAL.models import User, Student, Faculty, Exams, Location, Report
from .app_utils import createUsers, validateEmail

# setup the application and specify where the template folder is located
app = Flask(__name__, template_folder="../presentation/templates", static_folder="../presentation/static")
app.secret_key = "supersecretkey"

# Use SQLite in-memory database (temporary, erased when app stops)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_database(app=app)

# run script to add users
createUsers(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.context_processor
def inject_logged_in_user():
    return dict(loggedInUser=session.get('user'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        print(request.form)

        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("NSHEID")

        # Check if user already exists
        existing_user = Student.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.")
            return redirect(url_for("signup"))

        # Create and save new user with plain password
        new_user = Student(
            firstName=first_name,
            lastName=last_name,
            email=email,
            NSHEID=int(password)  # ❗ plain text password – only for testing!
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
        print(email)

        # if login was by student
        if validateEmail(email) == 1:
            user = Student.query.filter_by(email=email).first()

            if user is None: return redirect(url_for("login"))

            print(user.firstName)
            print(user.NSHEID, "===", password )

            if user and user.NSHEID == int(password):  # Ideally, hash and verify passwords!
                
                session['user'] = {
                    "id": user.id,
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "role": "student"
                }
                
                print(session['user'])
                return redirect(url_for("confirmation")) # Redirect to confirmation page
            else:
                print("FAIL")
                flash("Invalid login credentials.")
                return redirect(url_for("login"))
        # if login was by faculty
        elif validateEmail(email) == 2:
            user = Faculty.query.filter_by(email=email).first()

            if user is None: return redirect(url_for("login"))

            print(user)
            print(user.password, "===", password )

            if user and user.password == password:  # Ideally, hash and verify passwords!

                session['user'] = {
                    "id": user.id,
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "role": "faculty"
                }
                
                print(session['user'])
                return redirect(url_for("confirmation")) # Redirect to confirmation page
            else:
                print("FAIL")
                flash("Invalid login credentials.")
                return redirect(url_for("login"))
        else:
            print("FAIL")
            flash("Invalid login credentials.")
            return redirect(url_for("login"))

    return render_template("login.html")

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

    # Send faculty list to populate the dropdown
    faculty_list = Faculty.query.all()

    return render_template("filter.html", exams=results, faculty_list=faculty_list)

@app.route('/logout')
def logout():

    session.pop('user', None)  # Safely remove 'user' from session
    return redirect(url_for('login'))  # Redirect to login page

@app.route('/exam/<int:exam_id>')
def exam_detail(exam_id):
    exam = Exams.query.get_or_404(exam_id)
    loggedInUser = session.get('user')  # Safely get user from session
    return render_template("exam_detail.html", exam=exam, loggedInUser=loggedInUser)

# needs to be updated to allow only logged in faculty to view
@app.route("/faculty/report")
def faculty_report():
    return render_template("faculty/examReport.html")


@app.route('/exam/<int:exam_id>/register', methods=['POST'])
def register_exam(exam_id):
    student_id = request.form.get('studentId')  # Get from hidden input
    location_id = request.form.get('locationId')  # Optional, if still used

    student = Student.query.get(student_id)  # Lookup by primary key (id)
    exam = Exams.query.get_or_404(exam_id)

    if not student:
        print("Student not found.", "danger")
        return redirect(url_for('exam_detail', exam_id=exam_id))

    # Optional location check
    if location_id and str(exam.locationId) != str(location_id):
        print("Exam location mismatch.", "danger")
        return redirect(url_for('exam_detail', exam_id=exam_id))

    # Check if already registered
    existing = Report.query.filter_by(studentId=student.id, examId=exam.id).first()
    if existing:
        print("You're already registered for this exam.", "warning")
    else:
        new_report = Report(studentId=student.id, examId=exam.id)
        db.session.add(new_report)
        exam.examCount = (exam.examCount or 0) + 1
        db.session.commit()
        print("Registration successful!", "success")

    return redirect(url_for('exam_detail', exam_id=exam.id))

if __name__ == "__main__":
    app.run(debug=True)