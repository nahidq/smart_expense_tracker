from fastapi import FastAPI
from app.routers.expense_routes import router as expense_router
from app.database.db import Base, engine
from app.models.expense import  Expense
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(engine)
print("Tables created successfully!")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(expense_router)