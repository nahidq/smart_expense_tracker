from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Schema is owned by Alembic migrations now (run `alembic upgrade head`),
# so we no longer call Base.metadata.create_all() here.

def include_routers(app: FastAPI):
    from app.routes.auth_routes import router as auth_router
    from app.routes.user_routes import router as user_router
    from app.routes.health_routes import router as health_router

    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(health_router)

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
include_routers(app)
