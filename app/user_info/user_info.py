import os
import requests
import logging

logger = logging.getLogger(__name__)


class UserInfo:
    @staticmethod
    def get_current(x_pomerium_jwt_assertion: str):
        logger.info(f"Retrieving current user info")
        response = requests.get(
            url=os.getenv("USER_INFO_SERVICE_ENDPOINT") + f"/me",
            headers={"X-Pomerium-Jwt-Assertion": x_pomerium_jwt_assertion},
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get(user_id: str):
        logger.info(f"Retrieving user info for {user_id}")
        response = requests.get(
            url=os.getenv("USER_INFO_SERVICE_ENDPOINT") + f"/{user_id}",
        )
        response.raise_for_status()
        return response.json()
