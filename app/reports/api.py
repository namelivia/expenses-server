from fastapi import APIRouter, Depends, Header
from typing import Optional
from app.dependencies import get_db
from .report import Report, generate_expenses_report_en
from sqlalchemy.orm import Session

router = APIRouter(prefix="/reports", dependencies=[Depends(get_db)])


@router.get("", response_model=Report)
def report(
    db: Session = Depends(get_db),
    page: int = 0,
    x_pomerium_jwt_assertion: Optional[str] = Header(None),
):
    return generate_expenses_report_en(db)
