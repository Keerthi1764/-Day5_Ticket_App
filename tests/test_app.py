
import pytest

from app import app, reset_tickets


@pytest.fixture
def client():
    reset_tickets()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_list_tickets_returns_200(client):
    response = client.get("/api/tickets")
    assert response.status_code == 200
    assert len(response.get_json()) == 5


def test_get_ticket_1_has_a_title(client):
    response = client.get("/api/tickets/1")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Laptop not charging"


def test_unknown_ticket_returns_404(client):
    response = client.get("/api/tickets/9999")
    assert response.status_code == 404


# Bug 1: Test ticket priority sorting
def test_tickets_sorted_by_priority(client):
    response = client.get("/api/tickets")

    priorities = [
        ticket["priority"]
        for ticket in response.get_json()
    ]

    assert priorities == [
        "High", "High", "Medium", "Medium", "Low"
    ]


# Bug 2: Test empty title validation
def test_empty_title_returns_400(client):
    response = client.post(
        "/api/tickets",
        json={
            "title": "",
            "description": "Printer problem",
            "category": "Hardware",
            "priority": "High"
        }
    )

    assert response.status_code == 400


# Bug 3: Test resolved status on screen
def test_resolved_ticket_shows_resolved_on_screen(client):
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert '<td><span class="badge">Resolved</span></td>' in html
