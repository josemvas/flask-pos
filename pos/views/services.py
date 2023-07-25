from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from pos.models import db, Service

bp = Blueprint("services", __name__, url_prefix='/services')

@bp.route("/")
@login_required
def list():
    services = Service.query.all()
    return render_template("services/list.html", services=services)

@bp.route("/add", methods=["GET","POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template("services/form_add.html")
    service_name = request.form["service_name"]
    hourly_price = request.form["hourly_price"]
    service = Service()
    service.name = service_name
    service.hourly_price = hourly_price
    db.session.add(service)
    db.session.commit()
    return redirect(url_for("services.list"))

@bp.route("/edit", methods=["GET","POST"])
@login_required
def edit():
    if request.method == "GET":
        service_id = request.args["id"]
        service = Service.query.get(service_id)
        return render_template("services/form_edit.html", service=service)
    service_id = request.args["id"]
    service_name = request.form["service_name"]
    hourly_price = request.form["hourly_price"]
    service = Service.query.get(service_id)
    service.name = service_name
    service.hourly_price = hourly_price
    db.session.commit()
    return redirect(url_for("services.list"))

@bp.route("/delete", methods=["GET"])
@login_required
def delete():
    service_id = request.args["id"]
    service = Service.query.get(service_id)
    db.session.delete(service)
    db.session.commit()
    return redirect(url_for("services.list"))
