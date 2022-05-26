from pydantic.dataclasses import dataclass


@dataclass
class Report:
    content: str


def generate_expenses_report(total_this_month: float) -> Report:
    return Report(content=f"Total spent this month {total_this_month}")
