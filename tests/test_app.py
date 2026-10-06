import pytest
from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    return app.test_client()


def make(client, **over):
    data = {"amount": 120.5, "category": "food", "description": "Lunch", "date": "2026-10-01"}
    data.update(over)
    return client.post("/api/expenses", json=data)


def test_add_and_list(client):
    r = make(client)
    assert r.status_code == 201
    assert r.get_json()["category"] == "Food"
    assert len(client.get("/api/expenses").get_json()) == 1


@pytest.mark.parametrize("bad", [
    {"amount": "abc"}, {"amount": -5}, {"category": "Nope"},
    {"description": ""}, {"date": "01-10-2026"}])
def test_validation_errors(client, bad):
    assert make(client, **bad).status_code == 400


def test_summary(client):
    make(client, amount=100)
    make(client, amount=50, category="Bills")
    s = client.get("/api/summary").get_json()
    assert s["total"] == 150 and s["by_category"]["Food"] == 100


def test_delete_and_404(client):
    eid = make(client).get_json()["id"]
    assert client.delete(f"/api/expenses/{eid}").status_code == 204
    assert client.delete(f"/api/expenses/{eid}").status_code == 404


def test_home_page(client):
    assert b"Expense Tracker" in client.get("/").data
