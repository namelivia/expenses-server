from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    user_id = Column(String)
    user_name = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    group = Column(String)
    date = Column(DateTime, nullable=False, server_default=func.now())

    category = relationship(
        "app.categories.models.Category", back_populates="expense_list"
    )
