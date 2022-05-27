from mock import patch, Mock
from .test_base import (
    client,
    create_test_database,
    database_test_session,
)
from app.expenses.models import Expense
from app.categories.models import Category
from app.tasks.tasks import Tasks
import datetime
from freezegun import freeze_time


@freeze_time("2013-04-09")
class TestApp:
    def _insert_test_expense(self, session, expense: dict = {}):
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
    def test_sending_expenses_report(self, m_send_notification, database_test_session):
        self._insert_test_category(database_test_session, {"name": "Other category"})
        self._insert_test_expense(database_test_session)
        self._insert_test_expense(database_test_session)
        self._insert_test_expense(database_test_session)
        # Make sure expenses are filtered by month and year
        self._insert_test_expense(
            database_test_session,
            {"date": datetime.datetime.now() - datetime.timedelta(days=365)},
        )
        self._insert_test_category(database_test_session)
        self._insert_test_expense(database_test_session, {"category_id": 2})
        with freeze_time("2013-04-13"):
            Tasks.send_report(database_test_session)
        m_send_notification.assert_called_with(
            "6.00 spent on Other category | 2.00 spent on Test category | Total spent this month 8.00"
        )
