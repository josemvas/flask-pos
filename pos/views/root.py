from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, login_user, logout_user
from datetime import datetime, timedelta
from pos.models import db, User, Service, Transaction
from pos.auth import login_manager

bp = Blueprint("root", __name__)
login_manager.login_view = "root.login"

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("form_login.html")
    username = request.form["username"]
    password = request.form["password"]
    next_page = request.args.get("next")
    user = User.query.filter_by(name=username).one_or_none()
    if user:
        if user.verify_password(password):
            login_user(user)
            if next_page:
                return redirect(next_page)
            else:
                return render_template("display.html", message=f"Welcome {username}")
        else:
            return render_template("display.html", message="Wrong password")
    else:
        return render_template("display.html", message="Invalid user")

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("root.login"))

@bp.route("/pay", methods=["GET"])
@login_required
def pay():
    service_name = request.args["service"]
    start_time = request.args["start"]
    datetime_format = "%Y-%m-%d %H:%M"
    service = Service.query.filter_by(name=service_name).one_or_none()
    if service is None:
        abort(400)
    datetime_start = datetime.strptime(start_time, datetime_format)
    datetime_end = datetime.now().replace(second=0, microsecond=0)
    timedelta = datetime_end - datetime_start
    end_time = datetime_end.strftime(datetime_format)
    seconds = timedelta.total_seconds()
    price = max(seconds/3600, 0.5)*service.hourly_price
    return render_template("form_pay.html", service=service.name, seconds=seconds, price=price)
