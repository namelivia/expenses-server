from pydantic import BaseModel, Field


class UserData(BaseModel):
    id: int
    user_id: str = Field(title="User id on the identity provider")
    group: str = Field(title="Group for the user")

    class Config:
        orm_mode = True
