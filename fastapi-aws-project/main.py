from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routers import books, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Cloud Library API",
    description="API REST desplegable en AWS EC2 y conectada a Amazon RDS PostgreSQL.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(users.router)
app.include_router(books.router)


@app.get("/", tags=["Estado"])
def root():
    return {
        "status": "online",
        "message": "FastAPI está funcionando y conectado a PostgreSQL",
    }


@app.get("/health", tags=["Estado"])
def health():
    return {"status": "ok"}

