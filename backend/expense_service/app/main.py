from fastapi import FastAPI
from app.routers.expense_routes import router as expense_router
from fastapi.middleware.cors import CORSMiddleware

# Schema is owned by Alembic migrations now (run `alembic upgrade head`),
# so no longer call Base.metadata.create_all() is needed here.
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