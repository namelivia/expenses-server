import pytest
from mock import patch, Mock, call
from .test_base import (
    client,
    create_test_database,
    database_test_session,
)
from app.expenses.models import Expense
from app.users.models import UserData
from app.categories.models import Category
from app.expenses.schemas import Expense as ExpenseSchema
from app.expenses.crud import generate_report
import datetime
from freezegun import freeze_time


@freeze_time("2013-04-09")
class TestApp:
    def _insert_test_expense(self, session, expense: dict = {}):
        self._insert_test_category(session)
        data = {
            "name": "Test expense",
            "value": 200,
            "user_id": "some/user",
            "user_name": "Some user",
            "category_id": 1,
            "date": datetime.datetime.now(),
            "group": "Test group",
        }
        data.update(expense)
        db_expense = Expense(**data)
        session.add(db_expense)
        session.commit()
        return db_expense

    def _insert_test_user_data(self, session, user_data: dict = {}):
        data = {
            "user_id": "Test user",
            "group": "Test group",
        }
        data.update(user_data)
        db_user_data = UserData(**data)
        session.add(db_user_data)
        session.commit()
        return db_user_data

    def _insert_test_category(self, session, category: dict = {}):
        data = {
            "name": "Test category",
        }
        data.update(category)
        db_category = Category(**data)
        session.add(db_category)
        session.commit()
        return db_category

    @patch("app.notifications.notifications.Notifications.send")
    @patch("app.users.service.UserService.get_current_user_group")
    @patch("app.users.service.UserInfo.get")
    def test_create_expense(
        self,
        m_get_user_info,
        m_get_user_group,
        m_send_notification,
        client,
        database_test_session,
    ):
        m_get_user_group.return_value = "Test group"
        m_get_user_info.return_value = {"name": "Test user"}
        self._insert_test_category(database_test_session)
        response = client.post(
            "/expenses",
            json={
                "name": "Test expense",
                "value": 200,
                "user_id": "some/user",
                "category_id": 1,
            },
        )
        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "name": "Test expense",
            "value": 200,
            "user_id": "some/user",
            "user_name": "Test user",
            "category_id": 1,
            "date": "2013-04-09T00:00:00",
            "group": "Test group",
            "category": {
                "id": 1,
                "name": "Test category",
            },
        }
        m_send_notification.assert_called_with("Test user spent 2.00 on Test expense")

    def test_get_non_existing_expense(self, client):
        response = client.get("/expenses/99")
        assert response.status_code == 404

    @patch("app.users.api.UserInfo.get_current")
    def test_get_current_user(self, m_get_user_info, client):
        m_get_user_info.return_value = {
            "aud": ["example"],
            "email": "user@example.com",
            "exp": 1237658,
            "iat": 1237658,
            "iss": "test.example.com",
            "nbf": 1237658,
            "sub": "user",
            "name": "User Name",
        }
        response = client.get(
            "/users/me", headers={"X-Pomerium-Jwt-Assertion": "jwt_assertion"}
        )
        assert response.status_code == 200
        assert response.json() == {
            "aud": ["example"],
            "email": "user@example.com",
            "exp": 1237658,
            "iat": 1237658,
            "iss": "test.example.com",
            "nbf": 1237658,
            "sub": "user",
            "group": None,
            "name": "User Name",
        }
        m_get_user_info.assert_called_with("jwt_assertion")

    def test_get_existing_expense(self, client, database_test_session):
        self._insert_test_expense(database_test_session)
        response = client.get("/expenses/1")
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "Test expense",
            "value": 200,
            "user_id": "some/user",
            "user_name": "Some user",
            "category_id": 1,
            "date": "2013-04-09T00:00:00",
            "group": "Test group",
            "category": {
                "id": 1,
                "name": "Test category",
            },
        }

    def test_create_expense_invalid(self, client):
        response = client.post("/expenses", json={"payload": "Invalid"})
        assert response.status_code == 422

    @patch("app.users.service.UserService.get_current_user_group")
    def test_get_all_expenses(self, m_get_user_group, client, database_test_session):
        m_get_user_group.return_value = "Test group"
        self._insert_test_expense(database_test_session)
        self._insert_test_expense(database_test_session)
        response = client.get("/expenses")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "name": "Test expense",
                "value": 200,
                "user_id": "some/user",
                "user_name": "Some user",
                "category_id": 1,
                "date": "2013-04-09T00:00:00",
                "group": "Test group",
                "category": {
                    "id": 1,
                    "name": "Test category",
                },
            },
            {
                "id": 2,
                "name": "Test expense",
                "value": 200,
                "user_id": "some/user",
                "user_name": "Some user",
                "category_id": 1,
                "date": "2013-04-09T00:00:00",
                "group": "Test group",
                "category": {
                    "id": 1,
                    "name": "Test category",
                },
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
                "user_id": "some/user",
                "user_name": "Some user",
                "category_id": 1,
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "Updated name",
            "value": 200,
            "user_id": "some/user",
            "user_name": "Some user",
            "category_id": 1,
            "date": "2013-04-09T00:00:00",
            "group": "Test group",
            "category": {
                "id": 1,
                "name": "Test category",
            },
        }

    @patch("app.users.service.UserService.get_current_user_group")
    @patch("app.users.api.UserInfo.get")
    def test_get_totals(
        self, m_get_user_info, m_get_user_group, client, database_test_session
    ):
        m_get_user_group.return_value = "Test group"
        m_get_user_info.return_value = {"name": "Test user"}
        self._insert_test_user_data(database_test_session, {"user_id": "user_1"})
        self._insert_test_user_data(database_test_session, {"user_id": "user_2"})
        self._insert_test_expense(database_test_session, {"user_id": "user_1"})
        self._insert_test_expense(database_test_session, {"user_id": "user_1"})
        self._insert_test_expense(database_test_session, {"user_id": "user_2"})
        response = client.get("/expenses/totals")
        assert response.status_code == 200
        assert response.json() == [
            {
                "user": "Test user",
                "total": 400,
            },
            {
                "user": "Test user",
                "total": 200,
            },
        ]
        m_get_user_info.assert_has_calls([call("user_1"), call("user_2")])

    @patch("app.users.service.UserService.get_current_user_group")
    @patch("app.users.api.UserInfo.get")
    def test_get_users(
        self, m_get_user_info, m_get_user_group, client, database_test_session
    ):
        m_get_user_group.return_value = "Test group"
        m_get_user_info.return_value = {"name": "Test user"}
        self._insert_test_user_data(database_test_session, {"user_id": "user_1"})
        self._insert_test_user_data(database_test_session, {"user_id": "user_2"})
        response = client.get("/users")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "user_id": "user_1",
                "group": "Test group",
                "name": "Test user",
            },
            {
                "id": 2,
                "user_id": "user_2",
                "group": "Test group",
                "name": "Test user",
            },
        ]
        m_get_user_info.assert_has_calls([call("user_1"), call("user_2")])

    def test_get_categories(self, client, database_test_session):
        self._insert_test_category(database_test_session)
        self._insert_test_category(database_test_session)
        response = client.get("/categories")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "name": "Test category",
            },
            {
                "id": 2,
                "name": "Test category",
            },
        ]

    def test_create_category(self, client):
        response = client.post(
            "/categories",
            json={
                "name": "Test category",
            },
        )
        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "name": "Test category",
        }
