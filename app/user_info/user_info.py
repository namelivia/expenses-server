import os
import requests
import logging

logger = logging.getLogger(__name__)


class UserInfo:
    @staticmethod
    def get(x_pomerium_jwt_assertion: str):
        logger.info(f"Retrieving current user info")
        response = requests.get(
            url=os.getenv("USER_INFO_SERVICE_ENDPOINT") + f"/me",
            headers={"X-Pomerium-Jwt-Assertion": x_pomerium_jwt_assertion},
        )
        response.raise_for_status()
        return response.json()
