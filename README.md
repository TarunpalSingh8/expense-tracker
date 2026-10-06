# Expense Tracker

A portfolio-ready Python web app for recording and summarising personal expenses.
Built with **Flask** and **SQLite**, with a simple web UI and a REST API.

**Live demo:** <add your deployed link>  |  **Demo video:** <add your link>

## Features
- Add, list and delete expenses (web UI and REST API)
- Category-wise and total spending summary
- Input validation with clear error messages
- Exception handling with consistent JSON errors (400 / 404 / 500)
- Rotating log file (`logs/app.log`)
- Automated tests with pytest

## Architecture
```
expense-tracker/
├── app/
│   ├── __init__.py        # app factory + global error handlers
│   ├── routes.py          # HTTP layer (UI pages + REST endpoints)
│   ├── services.py        # business logic, validation, SQL queries
│   ├── db.py              # SQLite connection handling
│   ├── logging_config.py  # console + rotating file logging
│   ├── schema.sql         # database schema
│   └── templates/index.html
├── tests/test_app.py
├── run.py                 # local entry point
└── requirements.txt
```
Request flow: `routes` -> `services` (validate + query) -> `db` -> SQLite.
Errors raised in `services` (`ValidationError`, `NotFoundError`) are converted to HTTP responses centrally in `create_app`.

## Database schema
| Column      | Type    | Notes                     |
|-------------|---------|---------------------------|
| id          | INTEGER | primary key, autoincrement|
| amount      | REAL    | required, must be > 0     |
| category    | TEXT    | one of the fixed categories |
| description | TEXT    | required, max 100 chars   |
| date        | TEXT    | YYYY-MM-DD                |
| created_at  | TEXT    | default current timestamp |

## Setup
```bash
git clone <your-repo-url>
cd expense-tracker
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py                    # http://127.0.0.1:5000
```
Run tests: `pytest`

## API
| Method | Endpoint             | Description        |
|--------|----------------------|--------------------|
| GET    | /api/expenses        | List all expenses  |
| POST   | /api/expenses        | Create an expense  |
| GET    | /api/expenses/<id>   | Get one expense    |
| DELETE | /api/expenses/<id>   | Delete an expense  |
| GET    | /api/summary         | Totals by category |

Example:
```bash
curl -X POST http://127.0.0.1:5000/api/expenses \
  -H "Content-Type: application/json" \
  -d '{"amount": 250, "category": "Food", "description": "Dinner", "date": "2026-10-05"}'
```

## Deployment (Render)
Build command: `pip install -r requirements.txt`
Start command: `gunicorn run:app`

## Future improvements
User accounts, monthly charts, CSV export, PostgreSQL.
