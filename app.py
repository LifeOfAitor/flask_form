from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create the flask app with special keys and configuration
app = Flask(__name__)
app.config["SECRET_KEY"] = "myapp123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

# create the database related to the app with SQLAlchemy
db = SQLAlchemy(app)

# create database model
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))

@app.route("/", methods=["GET", "POST"])
def index():

    # if submit is pressed then get the information from the form
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_object = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        # create the db.Model
        form = Form(first_name=first_name, last_name=last_name, email=email,
                    date=date_object, occupation=occupation)

        # add data from the form to the database
        db.session.add(form)
        db.session.commit()
        flash(f"Form submitted {first_name}", "success")

    return render_template("index.html")

if __name__ == "__main__":
    # this will make the database if it does not exist
    with app.app_context():
        db.create_all()
    # runs the app
    app.run(debug=True, port=5001)