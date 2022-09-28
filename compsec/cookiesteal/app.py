from flask import Flask
from flask import (session, request, url_for, flash, g, redirect, render_template)
import random

app = Flask(__name__)
app.secret_key = "very secret debugging juice"

@app.route("/")
def hello_world():
    user_id = session.get("user_id")
    if user_id is not None:
        return "Hello " + str(user_id) + "<br> Your random login number is " + str(session.get("random"))
    return "hello stranger"

@app.route("/login")
def login():
    session["user_id"] = "admin"
    session["random"] = str(random.randint(1,10000))
    resp = redirect(url_for("hello_world"))
    resp.set_cookie("testcookie", "fillertext")
    return resp

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("hello_world"))

