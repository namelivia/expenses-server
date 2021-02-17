import os
import requests
import logging

logger = logging.getLogger(__name__)


class UserInfo:
    @staticmethod
    def get(user_id: str):
        logger.info(f"Retrieving info for user {user_id}")
        response = requests.get(
            url=os.getenv("USER_INFO_SERVICE_ENDPOINT") + f"/{user_id}"
        )
        response.raise_for_status()
        return response.text
