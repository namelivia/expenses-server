from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(title="Name for the category")


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True
