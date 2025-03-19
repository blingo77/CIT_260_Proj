from flask import Flask, jsonify
from flask import render_template
from DAL.database import db, init_database
from DAL.models import User

# setup the application and specify where the template folder is located
app = Flask(__name__, template_folder="../presentation/templates", static_folder="../presentation/static")

# Use SQLite in-memory database (temporary, erased when app stops)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_database(app=app)

@app.route('/')
def home():
    return render_template("index.html")

# This is required for the homepage to function
@app.route("/login")  # Make sure this exists!
def login():
    return render_template("login.html")


# This is required for the homepage to function
@app.route("/signup")  # Also define the signup page
def signup():
    return render_template("signup.html")

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