from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from app.expenses.api import router as expenses
from app.users.api import router as users
import logging
import sys

Base.metadata.create_all(bind=engine)

app = FastAPI()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

origins = ["http://localhost:8080", "http://expenses.namelivia.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

[
    app.include_router(router)
    for router in [
        expenses,
        users,
    ]
]
