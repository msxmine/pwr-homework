from flask import Flask, Blueprint, redirect, render_template, request, session, url_for, g, flash, abort
from passhash import check_password_hash, hash_password
import secrets
import sqlite3
import time
import datetime

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("./bank.db")
    return db

authbp = Blueprint('auth', __name__, url_prefix='/auth')

@authbp.route('/register', methods=('GET', 'POST'))
def registerpage():
    if request.method == 'POST':
        username = request.form['username'][:50]
        password = request.form['password'][:50]
        passwordrepeat = request.form['passwordconf'][:50]
        email = request.form['email'][:100]
        error = None
        db = get_db().cursor()

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif not email:
            error = "E-mail is required"
        elif password != passwordrepeat:
            error = "Passwords dont match"
        else:
            db.execute("SELECT id FROM user WHERE username = ?", (username,))
            if db.fetchone() is not None:
                error = "User {} is already registered".format(username)
        
        if error is None:
            db.execute("INSERT INTO user (username, password, email) VALUES (?, ?, ?)",
                        (username, hash_password(password), email))
            get_db().commit()
            flash("User created")
            return redirect(url_for("auth.loginpage"))

        flash(error)
    
    return render_template("auth/register.html")

@authbp.route('/login', methods=('GET', 'POST'))
def loginpage():
    if request.method == 'POST':
        username = request.form['username'][:50]
        password = request.form['password'][:50]
        error = None
        db = get_db().cursor()

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        else:
            db.execute("SELECT id,username,password FROM user WHERE username = ?", (username,))
            user = db.fetchone()

            if user is None:
                error = "Incorrect username"
            elif not check_password_hash(user[2], password):
                error = "Incorrect password"

            if error is None:
                session.clear()
                session["user_id"] = user[0]
                return redirect(url_for("mainpage"))

        flash(error)

    return render_template("auth/login.html")

@authbp.route("/requestpassreset", methods=('GET', 'POST'))
def passresetrequestpage():
    if request.method == 'POST':
        username = request.form['username'][:50]
        email = request.form['email'][:100]
        db = get_db().cursor()

        error = None
        if not username:
            error = "Wrong data"
        elif not email:
            error = "Wrong data"
        else:
            db.execute("SELECT id,username,email,lastresettime FROM user WHERE username = ? AND email = ?", (username,email,))
            user = db.fetchone()

            if user is None:
                error = "Wrong data"
            elif user[3] is not None and user[3] + 60 > int(time.time()):
                error = "Wait before trying again"
            else:
                secrettoken = secrets.token_hex(32)
                db.execute("UPDATE user SET lastresettime = ?, lastresetcode = ? WHERE id = ?", (int(time.time()), secrettoken, user[0],))
                get_db().commit()
                print("Secret token for", user[0], "is", secrettoken)
                session["recovering_id"] = user[0]
                return redirect(url_for("auth.passresetpage"))

        flash(error)
    
    return render_template("auth/requestpassreset.html")

@authbp.route("/passreset", methods=("GET", "POST"))
def passresetpage():
    if "recovering_id" not in session or session["recovering_id"] is None:
        return redirect(url_for("auth.passresetrequestpage"))

    rid = session["recovering_id"]

    if request.method == "POST":
        confcode = request.form["confcode"][:70]
        newpass = request.form["password"][:50]
        if not confcode:
            error = "Code required"
        elif not newpass:
            error = "Password required"
        else:
            db = get_db().cursor()
            db.execute("SELECT lastresettime, lastresetcode FROM user WHERE id = ?", (rid,))
            userdata = db.fetchone()
            if userdata is None:
                error = "User not found"
            elif userdata[0] + 3600 < int(time.time()):
                error = "Token no longer valid"
            elif userdata[1] != confcode:
                error = "Invalid token"
            else:
                db.execute("UPDATE user SET password = ?, lastresetcode = null WHERE id = ?", (hash_password(newpass), rid,))
                get_db().commit()
                session["recovering_id"] = None
                return redirect(url_for("auth.loginpage"))
        flash(error)
    
    return render_template("auth/confirmpassreset.html")

@authbp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_db().cursor()
        db.execute("SELECT id,username,email,type FROM user WHERE id = ?", (user_id,))
        dbres = db.fetchone()
        g.user = {"id": dbres[0], "username": dbres[1], "email": dbres[2], "type": dbres[3]}

@authbp.route("/logout")
def logoutpage():
    session.clear()
    return redirect(url_for("mainpage"))

transfersbp = Blueprint("transfers", __name__, url_prefix="/transfers")

@transfersbp.route("/transferspage")
def transferspage():
    if g.user is None:
        abort(403)
    
    db = get_db().cursor()
    db.execute("SELECT id,recvname,ammount,transferdate FROM transfers WHERE owner = ? ORDER BY transferdate DESC", (g.user["id"],))
    resul = list(db.fetchall())
    for i in range(len(resul)):
        resul[i] = list(resul[i])
        resul[i][2] = str(int(resul[i][2]) / 100.0 )
        resul[i][3] = str(datetime.datetime.fromtimestamp(resul[i][3]))
    return render_template("transfers/transferlist.html", transferlist=resul)

@transfersbp.route("/newtransfer", methods=("GET", "POST"))
def newtransfer():
    if g.user is None:
        abort(403)

    if request.method == "POST":
        error = None
        try:
            recvname = request.form["recvname"]
            recvaccnum = int(request.form["recvaccnum"])
            ammount = int(float(request.form["ammount"])*100)
        except:
            recvname = None
            recvaccnum = None
            ammount = None
        if not recvname or not recvaccnum or not ammount:
            error = "invalid input"
        else:
            session["confirmingtransfer"] = {
                "recvname": recvname,
                "recvaccnum": recvaccnum,
                "ammount": ammount
            }
            return redirect(url_for("transfers.confirmtransfer"))
        flash(error)

    return render_template("transfers/newtransfer.html")

@transfersbp.route("/confirmtransfer", methods=("GET", "POST"))
def confirmtransfer():
    if g.user is None:
        abort(403)

    confirmingdetails = session.get("confirmingtransfer")
    if (confirmingdetails is None or "recvname" not in confirmingdetails 
        or "recvaccnum" not in confirmingdetails or "ammount" not in confirmingdetails):
        return redirect(url_for("transfers.newtransfer"))

    if request.method == "POST":
        newdata = (g.user['id'], confirmingdetails["recvname"], str(confirmingdetails["recvaccnum"]), int(time.time()), confirmingdetails["ammount"],)
        db = get_db().cursor()
        db.execute("INSERT INTO transfers (owner,recvname,recvaccnum,transferdate,ammount) VALUES (?,?,?,?,?)", newdata)
        newid = db.lastrowid
        get_db().commit()
        return redirect(url_for("transfers.transferdetails", id=newid))

    displaydetails = []
    displaydetails.append(confirmingdetails["recvname"])
    displaydetails.append(str(confirmingdetails["recvaccnum"]))
    displaydetails.append(str(confirmingdetails["ammount"] / 100.0))
    return render_template("transfers/confirmtransfer.html", transfer=displaydetails)

@transfersbp.route("/details/<int:id>")
def transferdetails(id):
    if g.user is None:
        abort(403)
    db = get_db().cursor()
    db.execute("SELECT id,owner,recvname,recvaccnum,transferdate,ammount FROM transfers WHERE id = ? AND owner = ?", (id, g.user["id"],))
    res = db.fetchone()
    if not res:
        flash("No such transfer")
        redirect(url_for("transfers.transferspage"))
    
    displaydetails = []
    displaydetails.append(res[2])
    displaydetails.append(str(res[3]))
    displaydetails.append(str(res[5] / 100.0))
    displaydetails.append(str(datetime.datetime.fromtimestamp(res[4])))
    return render_template("transfers/transferdetails.html", transfer=displaydetails)

app = Flask(__name__)

@app.route("/")
def mainpage():
    return render_template("main.html")

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

app.register_blueprint(authbp)
app.register_blueprint(transfersbp)
app.secret_key = secrets.token_bytes(1024)

app.run(debug=True)
