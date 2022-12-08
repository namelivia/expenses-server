from pydantic.dataclasses import dataclass
import datetime
from sqlalchemy.orm import Session
from app.categories.crud import get_categories
from app.expenses.crud import get_total_by_category_during_month


@dataclass
class Report:
    content: str


def _get_category_name(category_id: int, categories) -> str:
    for category in categories:
        if category.id == category_id:
            return category.name
    # TODO: Raise an alert
    return "Unknown category"


def generate_expenses_report_en(db: Session) -> Report:
    this_month = datetime.datetime.now().month
    this_year = datetime.datetime.now().year
    total_by_category_this_month = get_total_by_category_during_month(
        db, this_month, this_year
    )
    categories = get_categories(db)
    content = ""
    for category in total_by_category_this_month:
        category_name = _get_category_name(category[0], categories)
        total_for_category = category[1] / 100
        content += f"{total_for_category:.2f} spent on {category_name} | "
    total = sum([category[1] for category in total_by_category_this_month]) / 100
    content += f"Total spent this month {total:.2f}"
    return Report(content=content)


def generate_expenses_report_es(db: Session) -> Report:
    this_month = datetime.datetime.now().month
    this_year = datetime.datetime.now().year
    total_by_category_this_month = get_total_by_category_during_month(
        db, this_month, this_year
    )
    categories = get_categories(db)
    content = ""
    for category in total_by_category_this_month:
        category_name = _get_category_name(category[0], categories)
        total_for_category = category[1] / 100
        content += f"{total_for_category:.2f} gastado en {category_name} | "
    total = sum([category[1] for category in total_by_category_this_month]) / 100
    content += f"Total gastado este mes {total:.2f}"
    return Report(content=content)
