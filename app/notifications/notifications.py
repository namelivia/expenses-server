import os
import requests
import logging

logger = logging.getLogger(__name__)


class Notifications:
    @staticmethod
    def get_endpoint_for_language(language: str) -> str:
        if language == "es":
            return os.getenv("NOTIFICATIONS_SERVICE_ENDPOINT")
        return None  # Currently only the Spanish endpoint is configured

    @staticmethod
    def send(language: str, message: str):
        logger.info(f"Sending notifications for language {language}")
        data = {"body": message}
        endpoint = Notifications.get_endpoint_for_language(language)
        if endpoint is None:
            logger.info(f"No endpoint configured for language {language}")
            return
        response = requests.post(url=endpoint, json=data)
        logger.info(response.text)
