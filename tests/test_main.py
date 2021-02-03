import pytest
from mock import patch, Mock
from .test_base import (
    client,
    create_test_database,
    database_test_session,
)
from app.expenses.models import Expense
from app.expenses.schemas import Expense as ExpenseSchema
import datetime
from freezegun import freeze_time


@freeze_time("2013-04-09")
class TestApp:
    def _insert_test_expense(self, session, expense: dict = {}):
        data = {
            "name": "Test expense",
            "value": 200,
            "user": "some user",
            "category": "some category",
            "date": datetime.datetime.now(),
        }
        data.update(expense)
        db_expense = Expense(**data)
        session.add(db_expense)
        session.commit()
        return db_expense

    @patch("app.notifications.notifications.Notifications.send")
    def test_create_expense(self, m_send_notification, client):
        response = client.post(
            "/expenses",
            json={
                "name": "Test expense",
                "value": 200,
                "user": "some user",
                "category": "some category",
            },
        )
        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "name": "Test expense",
            "value": 200,
            "user": "some user",
            "category": "some category",
            "date": "2013-04-09T00:00:00",
        }
        m_send_notification.assert_called_with(
            "A new expense called Test expense has been created"
        )

    def test_get_non_existing_expense(self, client):
        response = client.get("/expenses/99")
        assert response.status_code == 404

    @pytest.mark.skip(reason="no longer valid")
    def test_get_current_user(self, client):
        response = client.get("/users/me")
        assert response.status_code == 200
        assert response.json() == {
            "aud": ["example"],
            "email": "user@example.com",
            "exp": 1237658,
            "iat": 1237658,
            "iss": "test.example.com",
            "nbf": 1237658,
            "sub": "user",
        }

    def test_get_existing_expense(self, client, database_test_session):
        self._insert_test_expense(database_test_session)
        response = client.get("/expenses/1")
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "Test expense",
            "value": 200,
            "user": "some user",
            "category": "some category",
            "date": "2013-04-09T00:00:00",
        }

    def test_create_expense_invalid(self, client):
        response = client.post("/expenses", json={"payload": "Invalid"})
        assert response.status_code == 422

    def test_get_all_expenses(self, client, database_test_session):
        self._insert_test_expense(database_test_session)
        self._insert_test_expense(database_test_session)
        response = client.get("/expenses")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "name": "Test expense",
                "value": 200,
                "user": "some user",
                "category": "some category",
                "date": "2013-04-09T00:00:00",
            },
            {
                "id": 2,
                "name": "Test expense",
                "value": 200,
                "user": "some user",
                "category": "some category",
                "date": "2013-04-09T00:00:00",
            },
        ]

    def test_delete_non_existing_expense(self, client):
        response = client.get("/expenses/99")
        assert response.status_code == 404

    def test_delete_expense(self, client, database_test_session):
        self._insert_test_expense(database_test_session)
        response = client.get("/expenses/1")
        assert response.status_code == 200

    def test_updating_expense(self, client, database_test_session):
        original_expense = self._insert_test_expense(
            database_test_session, {"name": "Some name"}
        )
        response = client.put(
            "/expenses/1",
            json={
                "name": "Updated name",
                "value": 200,
                "user": "some user",
                "category": "some category",
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "Updated name",
            "value": 200,
            "user": "some user",
            "category": "some category",
            "date": "2013-04-09T00:00:00",
        }
