from pathlib import Path

from fastapi.testclient import TestClient


def test_production_frontend_routes_fall_back_to_index(client: TestClient) -> None:
    if not Path("frontend/admin_web/dist/index.html").exists():
        return

    response = client.get("/login")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_missing_static_asset_stays_404(client: TestClient) -> None:
    response = client.get("/favicon.ico")

    assert response.status_code == 404
