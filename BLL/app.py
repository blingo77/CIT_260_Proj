from flask import Flask, jsonify, request, url_for, flash, redirect
from flask import render_template
from DAL.database import db, init_database
from DAL.models import User, Student

# setup the application and specify where the template folder is located
app = Flask(__name__, template_folder="../presentation/templates", static_folder="../presentation/static")
app.secret_key = "supersecretkey"

# Use SQLite in-memory database (temporary, erased when app stops)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_database(app=app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Example logic (replace with your real user check)
        user = Student.query.filter_by(email=email).first()
        if user and user.password == password:  # Ideally, hash and verify passwords!
            return f"Welcome, {user.email}!"  # Redirect to dashboard, etc.
        else:
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



if __name__ == "__main__":
    app.run(debug=True)