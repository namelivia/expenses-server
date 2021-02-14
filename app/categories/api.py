from fastapi import APIRouter, Depends
from app.dependencies import get_db
from http import HTTPStatus
from . import crud, schemas
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(prefix="/categories", dependencies=[Depends(get_db)])


@router.get("", response_model=List[schemas.Category])
def categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    return categories


@router.post("", response_model=schemas.Category, status_code=HTTPStatus.CREATED)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
):
    return crud.create_category(db, category)
