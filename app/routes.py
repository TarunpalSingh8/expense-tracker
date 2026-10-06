from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from . import services

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return render_template("index.html", error=None, expenses=services.list_expenses(),
                           summary=services.summary(), categories=services.CATEGORIES)


@bp.post("/expenses")
def add_from_form():
    services.add_expense(request.form)
    return redirect(url_for("main.index"))


@bp.post("/expenses/<int:expense_id>/delete")
def delete_from_form(expense_id):
    services.delete_expense(expense_id)
    return redirect(url_for("main.index"))


# ---------- REST API ----------
@bp.get("/api/expenses")
def api_list():
    return jsonify(services.list_expenses())


@bp.post("/api/expenses")
def api_add():
    return jsonify(services.add_expense(request.get_json(silent=True) or {})), 201


@bp.get("/api/expenses/<int:expense_id>")
def api_get(expense_id):
    return jsonify(services.get_expense(expense_id))


@bp.delete("/api/expenses/<int:expense_id>")
def api_delete(expense_id):
    services.delete_expense(expense_id)
    return "", 204


@bp.get("/api/summary")
def api_summary():
    return jsonify(services.summary())
