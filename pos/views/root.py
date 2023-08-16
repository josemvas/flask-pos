from flask import Blueprint, render_template, session, request, redirect, url_for, abort
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
            session.permanent = True
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
    services = Service.query.all()
    hourly_prices = {service.name:service.hourly_price for service in services}
    selected_service = request.args["service"]
    start_time = request.args["start"]
    datetime_format = "%Y-%m-%d %H:%M"
    datetime_start = datetime.strptime(start_time, datetime_format)
    datetime_end = datetime.now().replace(second=0, microsecond=0)
    timedelta = datetime_end - datetime_start
    end_time = datetime_end.strftime(datetime_format)
    minutes = int(timedelta.total_seconds()//60)
    return render_template("form_pay.html", minutes=minutes, selected_service=selected_service, hourly_prices=hourly_prices)
