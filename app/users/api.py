from fastapi import Depends
from typing import Optional
from fastapi import APIRouter, Header
from sqlalchemy.orm import Session
from app.dependencies import get_db
import logging
from . import crud
from .jwt import JWT

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users")


@router.get("/me")
async def get_current_user(
    db: Session = Depends(get_db),
    x_pomerium_jwt_assertion: Optional[str] = Header(None),
):
    user_auth_data = JWT.get_current_user_info(x_pomerium_jwt_assertion)
    user_data = crud.get_or_create_user_data(db, user_auth_data["sub"])
    return {
        **user_auth_data,
        **{
            "group": user_data.group,
        },
    }
