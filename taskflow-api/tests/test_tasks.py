from tests.conftest import USER


def make(client, headers, **kw):
    payload = {"title": "Task"}
    payload.update(kw)
    return client.post("/tasks", json=payload, headers=headers)


def test_create_task_defaults(client, auth_headers):
    res = make(client, auth_headers, title="  Write tests  ")
    assert res.status_code == 201
    body = res.json()
    assert body["title"] == "Write tests"
    assert body["status"] == "pending"
    assert body["priority"] == "medium"


def test_create_task_empty_title(client, auth_headers):
    assert make(client, auth_headers, title="   ").status_code == 422


def test_create_task_invalid_status(client, auth_headers):
    assert make(client, auth_headers, status="bogus").status_code == 422


def test_get_task(client, auth_headers):
    tid = make(client, auth_headers).json()["id"]
    res = client.get(f"/tasks/{tid}", headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["id"] == tid


def test_get_missing_task(client, auth_headers):
    assert client.get("/tasks/999", headers=auth_headers).status_code == 404


def test_update_task(client, auth_headers):
    tid = make(client, auth_headers).json()["id"]
    res = client.patch(
        f"/tasks/{tid}", json={"status": "done", "priority": "high"}, headers=auth_headers
    )
    assert res.status_code == 200
    assert res.json()["status"] == "done"
    assert res.json()["priority"] == "high"
    assert res.json()["title"] == "Task"


def test_update_missing_task(client, auth_headers):
    res = client.patch("/tasks/999", json={"status": "done"}, headers=auth_headers)
    assert res.status_code == 404


def test_delete_task(client, auth_headers):
    tid = make(client, auth_headers).json()["id"]
    assert client.delete(f"/tasks/{tid}", headers=auth_headers).status_code == 204
    assert client.get(f"/tasks/{tid}", headers=auth_headers).status_code == 404


def test_delete_missing_task(client, auth_headers):
    assert client.delete("/tasks/999", headers=auth_headers).status_code == 404


def test_list_filters(client, auth_headers):
    make(client, auth_headers, title="a", status="done", priority="low", due_date="2026-01-01")
    make(client, auth_headers, title="b", status="pending", priority="high", due_date="2026-12-01")
    make(client, auth_headers, title="c", status="pending", priority="high")

    def titles(params):
        res = client.get("/tasks", params=params, headers=auth_headers)
        assert res.status_code == 200
        return sorted(t["title"] for t in res.json()["tasks"])

    assert titles({"status": "pending"}) == ["b", "c"]
    assert titles({"priority": "low"}) == ["a"]
    assert titles({"due_before": "2026-06-01"}) == ["a"]


def test_list_sort_and_pagination(client, auth_headers):
    for i in range(5):
        make(client, auth_headers, title=f"t{i}")
    res = client.get(
        "/tasks", params={"limit": 2, "page": 2, "sort": "created_at", "order": "asc"},
        headers=auth_headers,
    )
    body = res.json()
    assert body["total"] == 5
    assert body["page"] == 2
    assert [t["title"] for t in body["tasks"]] == ["t2", "t3"]


def test_list_invalid_params(client, auth_headers):
    assert client.get("/tasks", params={"sort": "bad"}, headers=auth_headers).status_code == 422
    assert client.get("/tasks", params={"limit": 1000}, headers=auth_headers).status_code == 422


def test_users_cannot_see_each_other_tasks(client, auth_headers):
    tid = make(client, auth_headers).json()["id"]
    other = {"email": "other@example.com", "password": "Password1"}
    client.post("/auth/register", json=other)
    token = client.post(
        "/auth/login", data={"username": other["email"], "password": other["password"]}
    ).json()["access_token"]
    h2 = {"Authorization": f"Bearer {token}"}
    assert client.get("/tasks", headers=h2).json()["total"] == 0
    assert client.get(f"/tasks/{tid}", headers=h2).status_code == 404
    assert client.delete(f"/tasks/{tid}", headers=h2).status_code == 404
