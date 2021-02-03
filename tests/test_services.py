from mock import patch
from app.notifications.notifications import Notifications


class TestServices:
    @patch("requests.post")
    def test_sending_a_notification(self, m_post):
        Notifications.send("Test message")
        m_post.assert_called_with(
            url="http://notifications-service:80",
            json={"message": "Test message"},
        )
