from mock import patch
from app.notifications.notifications import Notifications
from app.users.service import UserService
from app.users.models import UserData
from .test_base import (
    database_test_session,
)


class TestServices:
    @patch("requests.post")
    def test_sending_a_notification(self, m_post):
        Notifications.send("Test message")
        m_post.assert_called_with(
            url="http://notifications-service:80",
            json={"message": "Test message"},
        )

    @patch("app.users.jwt.JWT.get_current_user_info")
    def test_getting_current_user_group(
        self, m_get_current_user_info, database_test_session
    ):
        db_user_data = UserData(group="Test Group", user_id="user")
        database_test_session.add(db_user_data)
        database_test_session.commit()
        m_get_current_user_info.return_value = {
            "aud": ["example"],
            "email": "user@example.com",
            "exp": 1237658,
            "iat": 1237658,
            "iss": "test.example.com",
            "nbf": 1237658,
            "sub": "user",
        }
        group = UserService.get_current_user_group(
            database_test_session, "JWT assertion"
        )
        assert group == "Test Group"
