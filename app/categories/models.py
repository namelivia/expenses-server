from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

CategoriesBase = declarative_base()


class Category(CategoriesBase):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
