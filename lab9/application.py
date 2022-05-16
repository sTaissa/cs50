import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        if validation(month, day) == True:
            return renderIndex("Invalid birthday")

        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)
        return redirect("/")

    else: #if method is get
       return renderIndex('')

bid = ""
@app.route("/edit", methods=["GET", "POST"])
def edit():
    global bid
    if request.method == "GET":
        name = db.execute("SELECT name FROM birthdays WHERE id=?", request.args.get("id"))
        month = db.execute("SELECT month FROM birthdays WHERE id=?", request.args.get("id"))
        day = db.execute("SELECT day FROM birthdays WHERE id=?", request.args.get("id"))
        bid = request.args.get("id")
        return render_template("edit.html", name=name[0]['name'], month=month[0]['month'], day=day[0]['day'])

    else:
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        if validation(month, day) == True:
            return renderIndex("Invalid birthday")

        db.execute("UPDATE birthdays SET name = ?, month = ?, day = ? WHERE id = ?", name, month, day, bid)
        return redirect("/")

@app.route("/blank")
def delete():
    db.execute("DELETE FROM birthdays WHERE id = ?", request.args.get("id"))
    return redirect("/")

def renderIndex(msg):
    birthdays = db.execute("SELECT * FROM birthdays")
    return render_template("index.html", birthdays = birthdays, message = msg)

def validation(month, day):
    if int(month) > 12 or int(month) < 1 or int(day) > 31 or int(day) < 1:
        return True
