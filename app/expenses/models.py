from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

ExpensesBase = declarative_base()


class Expense(ExpensesBase):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    user = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    group = Column(String)
    date = Column(DateTime, nullable=False, server_default=func.now())

    category = relationship("Category", back_populates="expense_list")


class Category(ExpensesBase):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    expense_list = relationship("Expense", back_populates="category")
