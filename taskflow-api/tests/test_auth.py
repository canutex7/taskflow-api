from tests.conftest import USER


def test_register_success(client):
    res = client.post("/auth/register", json=USER)
    assert res.status_code == 201
    assert res.json()["email"] == USER["email"]
    assert "password" not in res.json()


def test_register_duplicate_email(client):
    client.post("/auth/register", json=USER)
    res = client.post("/auth/register", json=USER)
    assert res.status_code == 400


def test_register_weak_passwords(client):
    for pw in ["short1A", "alllowercase1", "NoNumbersHere"]:
        res = client.post("/auth/register", json={"email": "a@b.com", "password": pw})
        assert res.status_code == 422


def test_register_invalid_email(client):
    res = client.post("/auth/register", json={"email": "nope", "password": "Password1"})
    assert res.status_code == 422


def test_login_success(client):
    client.post("/auth/register", json=USER)
    res = client.post(
        "/auth/login", data={"username": USER["email"], "password": USER["password"]}
    )
    assert res.status_code == 200
    body = res.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"] and body["refresh_token"]


def test_login_wrong_password(client):
    client.post("/auth/register", json=USER)
    res = client.post("/auth/login", data={"username": USER["email"], "password": "Wrong123"})
    assert res.status_code == 401


def test_login_unknown_user(client):
    res = client.post("/auth/login", data={"username": "x@y.com", "password": "Password1"})
    assert res.status_code == 401


def test_refresh_success(client):
    client.post("/auth/register", json=USER)
    tokens = client.post(
        "/auth/login", data={"username": USER["email"], "password": USER["password"]}
    ).json()
    res = client.post("/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert res.status_code == 200
    assert res.json()["access_token"]


def test_refresh_rejects_access_token(client):
    client.post("/auth/register", json=USER)
    tokens = client.post(
        "/auth/login", data={"username": USER["email"], "password": USER["password"]}
    ).json()
    res = client.post("/auth/refresh", json={"refresh_token": tokens["access_token"]})
    assert res.status_code == 401


def test_refresh_invalid_token(client):
    res = client.post("/auth/refresh", json={"refresh_token": "garbage"})
    assert res.status_code == 401


def test_protected_route_requires_token(client):
    assert client.get("/tasks").status_code == 401


def test_protected_route_bad_token(client):
    res = client.get("/tasks", headers={"Authorization": "Bearer garbage"})
    assert res.status_code == 401


def test_health_and_root(client):
    assert client.get("/health").status_code == 200
    assert client.get("/").status_code == 200
