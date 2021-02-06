from sqlalchemy.orm import Session
import logging
from . import models

logger = logging.getLogger(__name__)


def get_categories(db: Session):
    return db.query(models.Category).all()
