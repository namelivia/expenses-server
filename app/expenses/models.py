from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

ExpensesBase = declarative_base()


class Expense(ExpensesBase):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    user = Column(String)
    category_name = Column(String)
    category_id = Column(Integer, nullable=True)
    group = Column(String)
    date = Column(DateTime, nullable=False, server_default=func.now())
