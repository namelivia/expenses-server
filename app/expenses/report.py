from typing import List
from pydantic.dataclasses import dataclass


@dataclass
class Report:
    content: str


def generate_expenses_report(expenses_by_category: List) -> Report:
    content = ""
    for category in expenses_by_category:
        content += f"{category[1]} spent on {category[0]} | "
    total = sum([category[1] for category in expenses_by_category])
    content += f"Total spent this month {total}"
    return Report(content=content)
