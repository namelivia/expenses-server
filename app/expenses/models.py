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
    category_name = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    group = Column(String)
    date = Column(DateTime, nullable=False, server_default=func.now())

    selected_category = relationship("Category", back_populates="expenses")


class Category(ExpensesBase):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    expenses = relationship("Expense", back_populates="selected_category")
