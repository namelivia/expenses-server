from . import crud
from app.user_info.user_info import UserInfo
import logging

logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    def get_current_user_group(db, x_pomerium_jwt_assertion):
        try:
            user_info = UserInfo.get(x_pomerium_jwt_assertion)
            user_data = crud.get_or_create_user_data(db, user_info["sub"])
            return user_data.group
        except Exception as err:
            logger.error(f"User info could not be retrieved: {str(err)}")

    @staticmethod
    def get_all_users_from_group(db, group):
        return crud.get_group_users(db, group)

    @staticmethod
    def get_current_user_name(db, x_pomerium_jwt_assertion):
        try:
            user_info = UserInfo.get(x_pomerium_jwt_assertion)
            return user_info.name
        except Exception as err:
            logger.error(f"User info could not be retrieved: {str(err)}")
