"""app/main.py — TaskFlow API application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, tasks

# Create all tables on startup (use Alembic for production migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskFlow API",
    description="A production-ready task management REST API with JWT auth.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "TaskFlow API is running. Visit /docs for the API reference."}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
