# TODO: Maybe the filename crud is not that good since this is not CRUD anymore
from sqlalchemy.orm import Session
import logging
import datetime
from . import models, schemas
from app.notifications.notifications import Notifications
from app.users.service import UserService

logger = logging.getLogger(__name__)


def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()


# TODO: skip and limit
# TODO: passing around the whole assertion is something I can avoid
def get_expenses(db: Session, x_pomerium_jwt_assertion):
    return (
        db.query(models.Expense)
        .filter(
            models.Expense.group
            == UserService.get_current_user_group(db, x_pomerium_jwt_assertion)
        )
        .all()
    )


def create_expense(
    db: Session, expense: schemas.ExpenseCreate, x_pomerium_jwt_assertion
):
    db_expense = models.Expense(
        **expense.dict(),
        date=datetime.datetime.now(),
        group=UserService.get_current_user_group(db, x_pomerium_jwt_assertion),
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    logger.info("New expense created")
    try:
        Notifications.send(
            f"{db_expense.user} spent {db_expense.value} on {db_expense.name}"
        )
    except Exception as err:
        logger.error(f"Notification could not be sent: {str(err)}")
    return db_expense


def update_expense(
    db: Session, expense_id: int, new_expense_data: schemas.ExpenseUpdate
):
    expenses = db.query(models.Expense).filter(models.Expense.id == expense_id)
    expenses.update(new_expense_data, synchronize_session=False)
    db.commit()
    expense = expenses.first()
    logger.info("Expense updated")
    try:
        Notifications.send(f"The expense {expense.name} has been updated")
    except Exception as err:
        logger.error(f"Notification could not be sent: {str(err)}")
    return expense


def delete_expense(db: Session, expense: models.Expense):
    db.delete(expense)
    db.commit()
    logger.info("Expense deleted")
