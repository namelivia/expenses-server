from sqlalchemy.orm import Session
import logging
from . import models

logger = logging.getLogger(__name__)


def get_or_create_user_data(db: Session, user_id: str):
    db_user_data = (
        db.query(models.UserData).filter(models.UserData.user_id == user_id).first()
    )
    if db_user_data is None:
        db_user_data = models.UserData(user_id=user_id)
        db.add(db_user_data)
        db.commit()
        db.refresh(db_user_data)
    return db_user_data


def get_group_users(db: Session, group: str):
    return db.query(models.UserData).filter(models.UserData.group == group).all()
