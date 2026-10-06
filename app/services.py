"""Business logic: validation and database operations."""
import logging
import sqlite3
from datetime import date as _date, datetime

from .db import get_db

log = logging.getLogger(__name__)
CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Health", "Entertainment", "Other"]


class ValidationError(ValueError):
    pass


class NotFoundError(LookupError):
    pass


def validate(data):
    try:
        amount = round(float(data.get("amount")), 2)
    except (TypeError, ValueError):
        raise ValidationError("Amount must be a number.")
    if amount <= 0:
        raise ValidationError("Amount must be greater than zero.")

    category = (data.get("category") or "").strip().title()
    if category not in CATEGORIES:
        raise ValidationError(f"Category must be one of: {', '.join(CATEGORIES)}.")

    description = (data.get("description") or "").strip()
    if not description or len(description) > 100:
        raise ValidationError("Description is required (max 100 characters).")

    when = (data.get("date") or _date.today().isoformat()).strip()
    try:
        datetime.strptime(when, "%Y-%m-%d")
    except ValueError:
        raise ValidationError("Date must be in YYYY-MM-DD format.")

    return amount, category, description, when


def add_expense(data):
    values = validate(data)
    try:
        db = get_db()
        cur = db.execute(
            "INSERT INTO expenses (amount, category, description, date) VALUES (?,?,?,?)",
            values)
        db.commit()
    except sqlite3.Error:
        log.exception("Database error while adding expense")
        raise
    log.info("Added expense id=%s amount=%s", cur.lastrowid, values[0])
    return get_expense(cur.lastrowid)


def get_expense(expense_id):
    row = get_db().execute("SELECT * FROM expenses WHERE id=?", (expense_id,)).fetchone()
    if row is None:
        raise NotFoundError(f"Expense {expense_id} not found.")
    return dict(row)


def list_expenses():
    rows = get_db().execute("SELECT * FROM expenses ORDER BY date DESC, id DESC").fetchall()
    return [dict(r) for r in rows]


def delete_expense(expense_id):
    get_expense(expense_id)  # raises NotFoundError if missing
    db = get_db()
    db.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    db.commit()
    log.info("Deleted expense id=%s", expense_id)


def summary():
    db = get_db()
    total = db.execute("SELECT COALESCE(SUM(amount),0) FROM expenses").fetchone()[0]
    rows = db.execute(
        "SELECT category, ROUND(SUM(amount),2) AS total FROM expenses "
        "GROUP BY category ORDER BY total DESC").fetchall()
    return {"total": round(total, 2), "by_category": {r["category"]: r["total"] for r in rows}}
