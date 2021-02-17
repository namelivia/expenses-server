from sqlalchemy import Column, Integer, String
from app.database import Base


class UserData(Base):
    __tablename__ = "user_data"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    group = Column(String, nullable=True)
