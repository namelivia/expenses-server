from fastapi import APIRouter, Path, HTTPException, Depends, Response
from http import HTTPStatus
from app.dependencies import get_db
from . import crud, schemas
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(prefix="/expenses", dependencies=[Depends(get_db)])


@router.get("", response_model=List[schemas.Expense])
def expenses(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    expenses = crud.get_expenses(db)
    return expenses


def _get_expense(db: Session, expense_id: int):
    db_expense = crud.get_expense(db, expense_id=expense_id)
    if db_expense is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Expense not found")
    return db_expense


@router.get("/{expense_id}", response_model=schemas.Expense)
def get_expense(
    expense_id: int = Path(None, title="The ID of the expense to get", ge=1),
    db: Session = Depends(get_db),
):
    return _get_expense(db, expense_id)


@router.post("", response_model=schemas.Expense, status_code=HTTPStatus.CREATED)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, expense)


@router.put("/{expense_id}", response_model=schemas.Expense, status_code=HTTPStatus.OK)
def update_expense(
    new_expense_data: schemas.ExpenseUpdate,
    db: Session = Depends(get_db),
    expense_id: int = Path(None, title="The ID for the expense to update", ge=1),
):
    return crud.update_expense(db, expense_id, new_expense_data)


@router.delete("/{expense_id}")
async def delete_expense(
    expense_id: int = Path(None, title="The ID of the expense to remove", ge=1),
    db: Session = Depends(get_db),
):
    crud.delete_expense(db, _get_expense(db, expense_id))
    return Response(status_code=HTTPStatus.NO_CONTENT)
