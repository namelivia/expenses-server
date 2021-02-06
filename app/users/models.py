from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

UserDataBase = declarative_base()


class UserData(UserDataBase):
    __tablename__ = "user_data"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    group = Column(String, nullable=True)
    name = Column(String, nullable=True)
