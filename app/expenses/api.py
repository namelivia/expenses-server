from fastapi import APIRouter, Path, HTTPException, Depends, Response, Header
from typing import Optional
from http import HTTPStatus
from app.dependencies import get_db
from . import crud, schemas
from typing import List
from sqlalchemy.orm import Session

expenses_router = APIRouter(prefix="/expenses", dependencies=[Depends(get_db)])


@expenses_router.get("", response_model=List[schemas.Expense])
def expenses(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    x_pomerium_jwt_assertion: Optional[str] = Header(None),
):
    expenses = crud.get_expenses(db, x_pomerium_jwt_assertion, skip, limit)
    return expenses


def _get_expense(db: Session, expense_id: int):
    db_expense = crud.get_expense(db, expense_id=expense_id)
    if db_expense is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Expense not found"
        )
    return db_expense


@expenses_router.get("/totals", response_model=List[schemas.Total])
def get_totals(
    db: Session = Depends(get_db),
    x_pomerium_jwt_assertion: Optional[str] = Header(None),
):
    totals = crud.get_totals(db, x_pomerium_jwt_assertion)
    return totals


@expenses_router.get("/{expense_id}", response_model=schemas.Expense)
def get_expense(
    expense_id: int = Path(None, title="The ID of the expense to get", ge=1),
    db: Session = Depends(get_db),
):
    return _get_expense(db, expense_id)


@expenses_router.post(
    "", response_model=schemas.Expense, status_code=HTTPStatus.CREATED
)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    x_pomerium_jwt_assertion: Optional[str] = Header(None),
):
    return crud.create_expense(db, expense, x_pomerium_jwt_assertion)


@expenses_router.put(
    "/{expense_id}", response_model=schemas.Expense, status_code=HTTPStatus.OK
)
def update_expense(
    new_expense_data: schemas.ExpenseUpdate,
    db: Session = Depends(get_db),
    expense_id: int = Path(None, title="The ID for the expense to update", ge=1),
):
    return crud.update_expense(db, expense_id, new_expense_data)


@expenses_router.delete("/{expense_id}")
async def delete_expense(
    expense_id: int = Path(None, title="The ID of the expense to remove", ge=1),
    db: Session = Depends(get_db),
):
    crud.delete_expense(db, _get_expense(db, expense_id))
    return Response(status_code=HTTPStatus.NO_CONTENT)


categories_router = APIRouter(prefix="/categories", dependencies=[Depends(get_db)])


@categories_router.get("", response_model=List[schemas.Category])
def categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    return categories


@categories_router.post(
    "", response_model=schemas.Category, status_code=HTTPStatus.CREATED
)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
):
    return crud.create_category(db, category)
