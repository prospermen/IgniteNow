from fastapi.testclient import TestClient

from backend.app.config import settings
from backend.app.models import Episode


ADMIN_HEADERS = {"X-Admin-Token": "demo-admin-token"}


def test_admin_reads_require_admin_token(client: TestClient, demo_episode: Episode) -> None:
    assert client.get("/api/dramas").status_code == 403
    assert client.get("/api/episodes").status_code == 403
    assert client.get(f"/api/episodes/{demo_episode.id}/highlights").status_code == 403

    assert client.get("/api/dramas", headers=ADMIN_HEADERS).status_code == 200
    assert client.get("/api/episodes", headers=ADMIN_HEADERS).status_code == 200
    assert client.get(f"/api/episodes/{demo_episode.id}/highlights", headers=ADMIN_HEADERS).status_code == 200


def test_admin_jwt_can_access_admin_reads(client: TestClient, demo_episode: Episode) -> None:
    create_response = client.post(
        "/api/auth/admin/users",
        headers=ADMIN_HEADERS,
        json={"username": "admin-user", "password": "secret123", "role": "admin"},
    )
    assert create_response.status_code == 200

    login_response = client.post("/api/auth/login", json={"username": "admin-user", "password": "secret123"})
    assert login_response.status_code == 200
    token = login_response.json()["data"]["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    assert client.get("/api/dramas", headers=headers).status_code == 200
    assert client.get(f"/api/episodes/{demo_episode.id}/highlights", headers=headers).status_code == 200


def test_auth_response_matches_frontend_contract(client: TestClient) -> None:
    create_response = client.post(
        "/api/auth/admin/users",
        headers=ADMIN_HEADERS,
        json={"username": "contract-admin", "password": "secret123", "role": "admin"},
    )
    assert create_response.status_code == 200

    login_response = client.post("/api/auth/login", json={"username": "contract-admin", "password": "secret123"})
    assert login_response.status_code == 200
    data = login_response.json()["data"]

    assert data["access_token"]
    assert data["token_type"] == "Bearer"
    assert data["expires_in"] == settings.jwt_expire_minutes * 60
    assert data["user"] == {
        "id": data["user_id"],
        "username": "contract-admin",
        "role": "admin",
    }
    assert data["username"] == "contract-admin"
    assert data["role"] == "admin"

    me_response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {data['access_token']}"})
    assert me_response.status_code == 200
    assert me_response.json()["data"]["user"]["role"] == "admin"

    logout_response = client.post("/api/auth/logout")
    assert logout_response.status_code == 200
    assert logout_response.json()["data"] == {"revoked": False}


def test_uploader_jwt_cannot_access_admin_reads(client: TestClient) -> None:
    register_response = client.post("/api/auth/register", json={"username": "uploader-2", "password": "secret123"})
    assert register_response.status_code == 200
    token = register_response.json()["data"]["access_token"]

    response = client.get("/api/dramas", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 403
    assert response.json()["detail"] == "admin role required"


def test_admin_managed_user_rejects_illegal_role(client: TestClient) -> None:
    response = client.post(
        "/api/auth/admin/users",
        headers=ADMIN_HEADERS,
        json={"username": "bad-role", "password": "secret123", "role": "owner"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "illegal role"
