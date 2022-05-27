from typing import List
from pydantic.dataclasses import dataclass


@dataclass
class Report:
    content: str


def _get_category_name(category_id: int, categories) -> str:
    for category in categories:
        if category.id == category_id:
            return category.name
    # TODO: Raise an alert
    return "Unknown category"


def generate_expenses_report(expenses_by_category: List, categories) -> Report:
    content = ""
    for category in expenses_by_category:
        category_name = _get_category_name(category[0], categories)
        content += f"{category[1]} spent on {category_name} | "
    total = sum([category[1] for category in expenses_by_category])
    content += f"Total spent this month {total}"
    return Report(content=content)
