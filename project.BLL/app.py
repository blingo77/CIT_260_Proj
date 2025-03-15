from flask import Flask
from flask import render_template

# setup the application and specify where the template folder is located
app = Flask(__name__, template_folder="../presentation/templates")

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)