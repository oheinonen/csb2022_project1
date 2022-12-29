from app import app
from flask import render_template, request, redirect,session, url_for
from db import db
import users, secret_repository

@app.route("/")
def index():
    sql = "SELECT secret,id FROM secrets"
    result = db.session.execute(sql)
    secrets = result.fetchall()
    return render_template("index.html", secrets=secrets)

@app.route("/add/secret",methods=["GET","POST"])
def add_secret():
    if request.method == "GET":
        return render_template("add_secret.html")
    if request.method == "POST":
        secret = request.form["secret"]
        if secret_repository.add_secret(secret):
            sql = "SELECT id FROM secrets WHERE secret=:secret ORDER BY id DESC LIMIT 1"
            result = db.session.execute(sql, {"secret":secret})
            id = result.fetchone()[0]
            return redirect(url_for('secret', id=id))
        else:
            return render_template("error.html", message = "Adding secret failed")

@app.route("/delete_account/<int:id>")
def delete_account(id):
    if users.delete_user(id):
        return redirect('/register')
    else:
        return render_template('error.html', message="You can only remove your own account")

@app.route("/secret/<int:id>")
def secret(id):
    sql = "SELECT secret FROM secrets WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    secret = result.fetchone()[0]
    return render_template("secret.html", id=id, secret=secret)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        if users.register(username,password, name):
            return redirect("/")
        else:
            return render_template("error.html",message="Registration failed")


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect("/")
        else:
            return render_template("error.html",message="Incorrect account details")

@app.route("/forgot_pass", methods=["GET","POST"])
def forgot_pass():
    if request.method == "GET":
        return render_template("forgot_pass.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        if users.login_without_pass(username, password, name):
            return redirect("/")
        else:
            return render_template("error.html",message="Incorrect account details")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")
