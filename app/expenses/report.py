from pydantic.dataclasses import dataclass


@dataclass
class Report:
    content: str
