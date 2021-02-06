from pydantic import BaseModel, Field
import datetime


class ExpenseBase(BaseModel):
    name: str = Field(title="Name for the expense")
    value: int = Field(title="Amount of money spent")
    user: str = Field(title="User that paid for the expense")
    category_name: str = Field(title="Category for the expense")
    category_id: int = Field(title="Category id for the expense")


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(ExpenseBase):
    pass


class Expense(ExpenseBase):
    id: int
    date: datetime.datetime = Field(title="Date for the expense")
    group: str = Field(title="Group for the expense")

    class Config:
        orm_mode = True


class Total(BaseModel):
    user: str = Field(title="User from the group")
    total: int = Field(title="Total amount paid")
