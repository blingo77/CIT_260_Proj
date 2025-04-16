from flask import Flask, jsonify, request, url_for, flash, redirect
from flask import render_template
from DAL.database import db, init_database
from DAL.models import User, Student
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
        email = request.form.get("email")
        validateEmail(email)

        password = request.form.get("password")
        print(email)

        # Example logic (replace with your real user check)
        user = Student.query.filter_by(email=email).first()
        print(user)
        print(user.NSHEID, "===", password )
        if user and user.NSHEID == int(password):  # Ideally, hash and verify passwords!
            print("SUCCESS")
            return redirect(url_for("confirmation")) # Redirect to confirmation page
        else:
            print("FAIL")
            flash("Invalid login credentials.")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route('/add_user', methods=['GET'])
def add_user():
    new_user = User(name="John Doe", email="john@example.com")
    db.session.add(new_user)
    db.session.commit()
    return f"User {new_user.name} added!"

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@app.route('/confirmation')
def confirmation():
    return render_template("confirmation.html")




if __name__ == "__main__":
    app.run(debug=True)