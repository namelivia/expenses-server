import os
import requests
import logging

logger = logging.getLogger(__name__)


class Notifications:
    @staticmethod
    def send(message: str):
        logger.info("Sending notification")
        data = {"body": message}
        response = requests.post(
            url=os.getenv("NOTIFICATIONS_SERVICE_ENDPOINT"), json=data
        )
        logger.info(response.text)
