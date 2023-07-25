from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from pos.models import db, User

bp = Blueprint("users", __name__, url_prefix='/users')

@bp.route("/")
@login_required
def list():
    users = User.query.all()
    return render_template("users/list.html", users=users)

@bp.route("/add", methods = ['GET', 'POST'])
@login_required
def add():
    if request.method == "GET":
        return render_template("users/form_add.html")
    username = request.form["username"]
    real_name = request.form["real_name"]
    password = request.form["password"]
    password2 = request.form["password2"]
    if password != password2:
        return render_template("display.html", "Passwords do not match")
    user = User()
    user.name = username
    user.real_name = real_name
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("users.list"))

@bp.route("/edit", methods=["GET","POST"])
@login_required
def edit():
    if request.method == "GET":
        user_id = request.args["id"]
        user = User.query.get(user_id)
        return render_template("users/form_edit.html", user=user)
    user_id = request.args["id"]
    real_name = request.form["real_name"]
    password = request.form["password"]
    password2 = request.form["password2"]
    if password != password2:
        return render_template("display.html", "Passwords do not match")
    user = User.query.get(user_id)
    user.real_name = real_name
    if password:
        user.hash_password(password)
    db.session.commit()
    return redirect(url_for("users.list"))

@bp.route("/delete", methods=["GET"])
@login_required
def delete():
    user_id = request.args["id"]
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("users.list"))
