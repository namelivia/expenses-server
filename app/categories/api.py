from fastapi import APIRouter, Depends
from app.dependencies import get_db
from . import crud, schemas
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(prefix="/categories", dependencies=[Depends(get_db)])


@router.get("", response_model=List[schemas.Category])
def categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    return categories
