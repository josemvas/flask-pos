from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from datetime import datetime, timedelta
from pos.models import db, Transaction, Service

bp = Blueprint("transactions", __name__, url_prefix='/transactions')

@bp.route("/")
@login_required
def list():
    transactions = Transaction.query.all()
    return render_template("transactions/list.html", transactions=transactions, now=datetime.now())

@bp.route("/add", methods=["GET","POST"])
@login_required
def add():
    if request.method == "GET":
        services = Service.query.all()
        return render_template("transactions/form_add.html", services=services)
    # ambil data dari form html
    service_name = request.form["service"]
    quantity = request.form["quantity"]
    duration = request.form["duration"]
    payment = request.form["payment"]
    # buat transacsi utamanya
    transaction = Transaction()
    service = Service.query.filter_by(name=service_name).one()
    transaction.service_id = service.id
    transaction.service_duration = duration
    transaction.service_quantity = quantity
    transaction.payment = payment
    db.session.add(transaction)
    db.session.flush()
    # commit semua transaksi
    db.session.commit()
    return redirect(url_for("transactions.list"))

@bp.route("/cancel", methods=["GET"])
@login_required
def cancel():
    transaction_id = request.args["id"]
    transaction = Transaction.query.get(transaction_id)
    if (datetime.now() - transaction.created_on).total_seconds()/60 < 15:
        transaction.status = "Canceled"
        db.session.add(transaction)
        db.session.commit()
    return redirect(url_for("transactions.list"))
