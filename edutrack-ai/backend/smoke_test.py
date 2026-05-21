"""Smoke test simples da API EduTrack."""
import json
import urllib.request
import urllib.error
import time

BASE = "http://localhost:5000/api"
EMAIL = f"smoke_{int(time.time())}@edu.com"
PASSWORD = "123456"


def req(method, path, data=None, token=None):
    url = f"{BASE}{path}"
    body = None
    headers = {"Content-Type": "application/json"}
    if data is not None:
        body = json.dumps(data).encode("utf-8")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8") or "{}")


def assert_ok(label, status, body, expected=200):
    ok = status == expected
    print(f"[{'OK' if ok else 'FAIL'}] {label} -> status={status} body={body}")
    if not ok:
        raise SystemExit(1)
    return body


def main():
    print(f"--- Smoke test ({EMAIL}) ---")
    s, b = req("POST", "/auth/register", {"email": EMAIL, "password": PASSWORD})
    assert_ok("register", s, b, 201)

    s, b = req("POST", "/auth/login", {"email": EMAIL, "password": PASSWORD})
    assert_ok("login", s, b, 200)
    token = b["access_token"]

    # Create subject
    s, b = req("POST", "/subjects", {
        "name": "Cálculo I",
        "professor": "Profa. Ana",
        "carga_horaria": 80,
        "peso": 1.5,
        "description": "Limites, derivadas e integrais.",
        "data_inicio": "2026-02-01",
        "data_fim": "2026-06-30"
    }, token)
    assert_ok("create subject", s, b, 201)
    subj_id = b["id"]

    s, b = req("GET", "/subjects", token=token)
    assert_ok("list subjects", s, b, 200)
    assert any(item["id"] == subj_id for item in b)

    # Update subject
    s, b = req("PUT", f"/subjects/{subj_id}", {"professor": "Profa. Ana Souza"}, token)
    assert_ok("update subject", s, b, 200)

    # Create tasks
    for t in [
        {"title": "Lista 1", "data_prevista": "2026-03-10", "status": "concluida"},
        {"title": "Lista 2", "data_prevista": "2026-03-20", "status": "pendente"},
        {"title": "Prova 1", "data_prevista": "2026-04-05", "status": "pendente", "description": "Avaliação parcial"},
    ]:
        s, b = req("POST", f"/tasks/{subj_id}", t, token)
        assert_ok(f"create task {t['title']}", s, b, 201)

    s, b = req("GET", f"/tasks/{subj_id}", token=token)
    assert_ok("list tasks", s, b, 200)
    tasks = b
    assert len(tasks) >= 3

    # Update one task status
    s, b = req("PUT", f"/tasks/{tasks[1]['id']}", {"status": "concluida"}, token)
    assert_ok("toggle task status", s, b, 200)

    # Delete one task
    s, b = req("DELETE", f"/tasks/{tasks[2]['id']}", token=token)
    assert_ok("delete task", s, b, 200)

    # Dashboard
    s, b = req("GET", "/dashboard", token=token)
    assert_ok("dashboard", s, b, 200)
    assert "weighted_progress" in b
    assert "total_carga_horaria" in b
    assert "subjects" in b and len(b["subjects"]) >= 1
    assert "prediction" in b
    assert "professor" in b["subjects"][0]
    print("Dashboard:", json.dumps(b, indent=2, ensure_ascii=False))

    # Cleanup
    s, b = req("DELETE", f"/subjects/{subj_id}", token=token)
    assert_ok("delete subject", s, b, 200)

    print("\nALL TESTS PASSED ✅")


if __name__ == "__main__":
    main()
