"""Test fixtures: isolated in-memory DB, test client, auth headers."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app import models  # noqa: F401  (registers models)

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


USER = {"email": "test@example.com", "password": "Password1"}


@pytest.fixture()
def auth_headers(client):
    client.post("/auth/register", json=USER)
    res = client.post(
        "/auth/login", data={"username": USER["email"], "password": USER["password"]}
    )
    return {"Authorization": f"Bearer {res.json()['access_token']}"}
