from .jwt import JWT
from . import crud


class UserService:
    @staticmethod
    def get_current_user_group(db, x_pomerium_jwt_assertion):
        user_auth_data = JWT.get_current_user_info(x_pomerium_jwt_assertion)
        user_data = crud.get_or_create_user_data(db, user_auth_data["sub"])
        return user_data.group
