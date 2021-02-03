import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_url():
    if os.environ.get("TESTING") == "True":
        return os.environ.get("TEST_DATABASE_URL")
    return os.environ.get("DATABASE_URL")


SQLALCHEMY_DATABASE_URL = get_url()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
