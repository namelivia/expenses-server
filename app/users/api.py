from fastapi import Depends
from typing import List
from typing import Optional
from fastapi import APIRouter, Header
from sqlalchemy.orm import Session
from app.dependencies import get_db
import logging
from . import crud, schemas
from .service import UserService
from app.user_info.user_info import UserInfo

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users")


@router.get("", response_model=List[schemas.UserData])
def get_users(
    db: Session = Depends(get_db),
    x_pomerium_jwt_assertion: Optional[str] = Header(None),
):
    group = UserService.get_current_user_group(db, x_pomerium_jwt_assertion)
    users = crud.get_group_users(db, group)
    return [{**user.__dict__, **UserInfo.get(user.user_id)} for user in users]


@router.get("/me")
async def get_current_user(
    db: Session = Depends(get_db),
    x_pomerium_jwt_assertion: Optional[str] = Header(None),
):
    try:
        user_info = UserInfo.get_current(x_pomerium_jwt_assertion)
        user_data = crud.get_or_create_user_data(db, user_info["sub"])
        return {
            **user_info,
            **{
                "group": user_data.group,
            },
        }
    except Exception as err:
        logger.error(f"User info could not be retrieved: {str(err)}")
