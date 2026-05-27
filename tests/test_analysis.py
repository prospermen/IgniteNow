from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.models import Episode


def test_login_required_for_analysis(client: TestClient, demo_episode: Episode) -> None:
    response = client.post(f"/api/episodes/{demo_episode.id}/analyze", json={"force_reanalyze": False})

    assert response.status_code == 401


def test_analysis_requires_subtitle_and_marks_episode_failed(
    client: TestClient,
    db_session: Session,
    demo_episode: Episode,
    uploader_headers: dict[str, str],
) -> None:
    response = client.post(
        f"/api/episodes/{demo_episode.id}/analyze",
        json={"force_reanalyze": False},
        headers=uploader_headers,
    )

    assert response.status_code == 400
    db_session.refresh(demo_episode)
    assert demo_episode.analyze_status == "failed"
    assert demo_episode.analyze_error == "subtitle is required"


def test_manual_highlight_rejects_time_after_episode_duration(
    client: TestClient,
    demo_episode: Episode,
    admin_headers: dict[str, str],
) -> None:
    response = client.post(
        f"/api/episodes/{demo_episode.id}/highlights",
        headers=admin_headers,
        json={
            "start_time": 29,
            "end_time": 40,
            "highlight_type": "suspense",
            "button_text": "快更",
            "effect": "countdown",
            "status": "draft",
        },
    )

    assert response.status_code == 400
    assert "duration" in response.json()["detail"]


def test_manual_highlight_rejects_illegal_effect(
    client: TestClient,
    demo_episode: Episode,
    admin_headers: dict[str, str],
) -> None:
    response = client.post(
        f"/api/episodes/{demo_episode.id}/highlights",
        headers=admin_headers,
        json={
            "start_time": 15,
            "end_time": 18,
            "highlight_type": "suspense",
            "button_text": "快更",
            "effect": "unknown",
            "status": "draft",
        },
    )

    assert response.status_code == 400
    assert "effect" in response.json()["detail"]
