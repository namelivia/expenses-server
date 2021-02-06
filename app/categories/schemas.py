from pydantic import BaseModel, Field


class Category(BaseModel):
    id: int
    name: str = Field(title="Name for the category")

    class Config:
        orm_mode = True
