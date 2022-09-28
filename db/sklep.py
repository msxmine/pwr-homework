from flask import Flask, Blueprint, redirect, render_template, request, session, url_for, g, flash, abort
import mariadb
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
import subprocess
	
authbp = Blueprint('auth', __name__, url_prefix='/auth')

@authbp.route('/register', methods=('GET', 'POST'))
def registerpage():
	if request.method == 'POST':
		username = request.form['username'][:50]
		password = request.form['password'][:50]
		error = None
		db = dbuserauth.cursor()
		
		if not username:
			error = "Username is required"
		elif not password:
			error = "Password is required"
		else:
			db.execute("SELECT id FROM user WHERE username = ?", (username,))
			if db.fetchone() is not None:
				error = "User {} is already registered".format(username)
		
		if error is None:
			db.execute("INSERT INTO user (username, password) VALUES (?, ?)",
			(username, generate_password_hash(password),))
			dbuserauth.commit()
			flash("User created")
			return redirect(url_for('auth.loginpage'))
		
		flash(error)
	
	return render_template("auth/register.html")
	
@authbp.route('/login', methods=('GET', 'POST'))
def loginpage():
	if request.method == 'POST':
		username = request.form['username'][:50]
		password = request.form['password'][:50]
		error = None
		db = dbuserauth.cursor()
		
		db.execute("SELECT id,username,password FROM user WHERE username = ?", (username,))
		user = db.fetchone()
		
		if user is None:
			error = "Incorrect username"
		elif not check_password_hash(user[2], password):
			error = "Incorrect password"
			
		if error is None:
			session.clear()
			session['user_id'] = user[0]
			return redirect(url_for('mainpage'))
		
		flash(error)
		
	return render_template("auth/login.html")
	
@authbp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')
	
	if user_id is None:
		g.user = None
	else:
		curs = dbuserauth.cursor()
		curs.execute("SELECT id,username,password,type FROM user WHERE id = ?", (user_id,))
		dbres = curs.fetchone()
		g.user = {"id": dbres[0], "username": dbres[1], "password": dbres[2], "type": dbres[3]}

@authbp.route("/logout")
def logoutpage():
	session.clear()
	return redirect(url_for('mainpage'))
	
@authbp.route("/delacc/<int:id>", methods=('GET', 'POST'))
def deleteaccountpage(id):
	if g.user is None:
		abort(403)
	if not (g.user['id'] == id or g.user['type'] == 2):
		abort(403)
		
	if request.method == 'POST':
		curs = dbuserauth.cursor()
		curs.execute("DELETE FROM user WHERE id = ?", (id,))
		dbuserauth.commit()
		session.clear()
		flash("Account deleted")
		return redirect(url_for('mainpage'))
	
	return render_template("auth/delete.html")
	
@authbp.route("/setpass/<int:id>", methods=('GET', 'POST'))
def setpasswordpage(id):
	if g.user is None:
		abort(403)
	if not (g.user['id'] == id or g.user['type'] == 2):
		abort(403)
		
	if request.method == 'POST':
		password = request.form['password'][:50]
		if not password:
			flash("Password is required")
			return render_template("auth/setpass.html")
			
		curs = dbuserauth.cursor()
		curs.execute("UPDATE user SET password = ? WHERE id = ?", (generate_password_hash(password),id,))
		dbuserauth.commit()
		flash("Password updated")
		return redirect(url_for('mainpage'))
	
	return render_template("auth/setpass.html")

@authbp.route("/settype/<int:id>", methods=('GET', 'POST'))
def settypepage(id):
	if g.user is None:
		abort(403)
	if not (g.user['type'] == 2):
		abort(403)
		
	if request.method == 'POST':
		try:
			newtype = int(request.form['type'])
		except:
			flash("bad value")
		else:
			curs = dbuserauth.cursor()
			curs.execute("UPDATE user SET type = ? WHERE id = ?", (newtype,id,))
			dbuserauth.commit()
			flash("Type updated")
			return redirect(url_for('auth.usermanagementpage'))
	
	return render_template("auth/settype.html")
	
	
@authbp.route("/usermanagement", methods=('GET', 'POST'))
def usermanagementpage():
	if g.user is None:
		abort(403)
		
	curs = dbuserauth.cursor()
	
	if request.method == 'POST':
		if g.user['type'] != 2:
			abort(403)
		filterstr = request.form['filterstr']
		curs.execute("SELECT id,username,type FROM user WHERE " + filterstr)
	else:
		if g.user['type'] == 2:
			curs.execute("SELECT id,username,type FROM user")
		else:
			curs.execute("SELECT id,username,type FROM user WHERE id = ?", (g.user['id'],))
	users = curs.fetchall()
	return render_template("auth/manage.html", users=users)



shopbp = Blueprint('shop', __name__, url_prefix='/shop')

@shopbp.route("/item/<int:id>", methods=('GET', 'POST'))
def itempage(id):
	curs = dbofferman.cursor()
	curs.execute("SELECT offer.id,user.username,offer.name,offer.description,offer.price,offer.qty,offer.sold,offer.owner FROM offer JOIN user ON offer.owner=user.id WHERE offer.id = ?", (id,))
	item = curs.fetchone()
	curs.close()
	if item is not None:
		if request.method == 'POST' and g.user is not None :
			qty = request.form['qty']
			if qty is None:
				qty = 1
			try:
				qty = int(qty)
			except:
				qty = 1
			if qty < 1:
				qty = 1
			curs = dbofferman.cursor()
			curs.execute("SELECT qty FROM cartitem WHERE offer = ? AND owner = ?", (id, g.user["id"],))
			prevqty = curs.fetchone()
			newrow = False
			curs.close()
			if prevqty is None:
				prevqty = 0
				newrow = True
			else:
				try:
					prevqty = int(prevqty[0])
				except:
					prevqty = 0
			
			curs = dbofferman.cursor()
			if newrow:
				curs.execute("INSERT INTO cartitem (offer,owner,qty) VALUES (?,?,?)", (id, g.user["id"], qty,))
			else:
				curs.execute("UPDATE cartitem SET qty = ? WHERE offer = ? AND owner = ?", ((qty+prevqty),id, g.user["id"],))
			dbofferman.commit()
			return redirect(url_for('mainpage'))
		else:
			return render_template("itemdetail.html", item=item)
	else:
		return redirect(url_for('mainpage'))
	
	
@shopbp.route("/user/<int:id>")
def shoppage(id):
	curs = dbofferman.cursor()
	curs.execute("SELECT offer.name,offer.price,user.username,offer.id FROM offer JOIN user ON offer.owner=user.id WHERE offer.qty > 0 AND offer.owner = ? ORDER BY name ASC", (id,))
	items = curs.fetchall()
	return render_template('usershop.html', items=items, shopid=id)
	
@shopbp.route("/user/<int:id>/additem", methods=('GET', 'POST'))
def additempage(id):
	if g.user is None:
		abort(403)
	if not ((g.user['id'] == id and g.user['type'] == 1) or g.user['type'] == 2):
		abort(403)
	
	if request.method == 'POST':
		name = request.form['name'][:250]
		desc = request.form['desc'][:8000]
		price = request.form['price']
		qty = request.form['qty']
		
		if name is None:
			return render_template("newitem.html")
		if desc is None:
			desc = ""
		if price is None:
			return render_template("newitem.html")
		if qty is None:
			qty = 1
			
		try:
			price = float(price)
			qty = int(qty)
		except:
			return render_template("newitem.html")
		
		if price < 0:
			price = 0;
		if qty < 0:
			qty = 0
			
		curs = dbofferman.cursor()
		try:
			curs.execute("INSERT INTO offer (owner,name,description,price,qty) VALUES (?,?,?,?,?)", (id, name, desc, price, qty,))
		except mariadb.OperationalError:
			flash("Vendor has too many listings")
			return redirect(url_for("shop.shoppage", id=id))
		else:
			dbofferman.commit()
			flash("Item added")
			return redirect(url_for("shop.shoppage", id=id))
		
	
	return render_template("newitem.html")

@shopbp.route("/item/<int:id>/delitem", methods=('GET', 'POST'))
def itemdelpage(id):
	if g.user is None:
		abort(403)
		
	curs = dbofferman.cursor()
	curs.execute("SELECT owner FROM offer WHERE id = ?", (id,))
	owner = curs.fetchone()
	if owner is None:
		return redirect(url_for('mainpage'))
	curs.close()
	
	if not (g.user['id'] == owner[0] or g.user['type'] == 2):
		abort(403)
		
	if request.method == 'POST':
		curs = dbofferman.cursor()
		curs.execute("DELETE FROM offer WHERE id = ?", (id,))
		dbofferman.commit()
		
		flash("Item deleted")
		return redirect(url_for('mainpage'))
	
	return render_template("delitem.html")
	
@shopbp.route("/searchresults", methods=('GET', 'POST'))
def searchpage():
	if request.method == 'POST':
		query = request.form['query'][:300]
		
		if query is not None:
			curs = dbofferman.cursor()
			curs.execute("PREPARE searchStmt FROM 'SELECT offer.name,offer.price,user.username,offer.id FROM offer JOIN user ON offer.owner=user.id WHERE LOCATE(?,offer.name) '")
			curs.callproc("searchProc", (query,))
			results = curs.fetchall()
			return render_template("searchresults.html", items=results)
			
	return redirect(url_for(mainpage))
	
@shopbp.route("/sellers")
def sellerspage():
	curs = dbofferman.cursor()
	curs.execute("SELECT username,id FROM user WHERE type = 1 ORDER BY username ASC")
	sellers = curs.fetchall()
	return render_template('sellerlist.html', sellers=sellers)
	
@shopbp.route("/cart", methods=('GET', 'POST'))
def cartpage():
	if g.user is None:
		return redirect(url_for(mainpage))
	
	
	
	if request.method == 'POST' and request.form['action'] is not None:
		if request.form['action'] == "Buy":
			curs = dbofferman.cursor()
			try:
				curs.callproc("commitCart", (g.user["id"],))
			except mariadb.OperationalError:
				flash("Not enough stock")
			dbofferman.commit()
			curs.close()
		if request.form['action'] == "Empty":
			curs = dbofferman.cursor()
			curs.execute("DELETE FROM cartitem WHERE owner = ?", (g.user["id"],))
			dbofferman.commit()
			curs.close()

	curs = dbofferman.cursor()
	curs.execute("SELECT offer.name,offer.price,user.username,offer.id,cartitem.qty FROM cartitem JOIN offer ON cartitem.offer=offer.id JOIN user ON offer.owner=user.id WHERE cartitem.owner = ?", (g.user["id"],))
	content = curs.fetchall()
	return render_template("cart.html", items=content)
	
adminbp = Blueprint('admin', __name__, url_prefix='/admin')

@adminbp.route("/", methods=('GET', 'POST'))
def adminpage():
	if g.user is None:
		abort(403)
	if not (g.user['type'] == 2):
		abort(403)
		
	if request.method == 'POST':
		if request.form['action'] == "Backup":
			subprocess.run(["bash", "./dbback.sh"])
		if request.form['action'] == "Restore":
			subprocess.run(["bash", "./dbrestore.sh"])
	return render_template("admin/adminpage.html")

app = Flask(__name__)

@app.route('/')
def mainpage():
	curs = dbofferman.cursor()
	curs.execute("SELECT offer.name,offer.price,user.username,offer.id FROM offer JOIN user ON offer.owner=user.id WHERE offer.qty > 0 ORDER BY offer.sold DESC LIMIT 20")
	items = curs.fetchall()
	return render_template('main.html', items=items)
	
app.register_blueprint(authbp)
app.register_blueprint(shopbp)
app.register_blueprint(adminbp)
app.secret_key = secrets.token_bytes(1024)

dbofferman = mariadb.connect(user="shopusr", host="localhost", password="buyconsume", port=3306, database="Webstore", autocommit=True)
dbuserauth = mariadb.connect(user="authusr", host="localhost", password="verysecure", port=3306, database="Webstore", autocommit=True)
app.run(debug=True)

