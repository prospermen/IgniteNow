import sys
from pathlib import Path

from sqlalchemy.orm import Session

from ..models import Episode, HighlightEvent
from .highlight_service import create_highlight


def analyze_episode_highlights(db: Session, episode: Episode, force_reanalyze: bool = False) -> dict:
    if episode.analyze_status == "processing":
        raise ValueError("episode is already processing")
    if not (episode.subtitle_content or episode.subtitle_url):
        episode.analyze_status = "failed"
        episode.analyze_error = "subtitle is required"
        db.commit()
        raise ValueError("subtitle is required")

    existing = db.query(HighlightEvent).filter(HighlightEvent.episode_id == episode.id).count()
    if existing and episode.analyze_status == "success" and not force_reanalyze:
        return {"highlight_count": existing, "existing": True}

    episode.analyze_status = "processing"
    episode.analyze_error = ""
    db.commit()

    try:
        repo_root = Path(__file__).resolve().parents[3]
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))
        from ai_service.highlight_analyzer import analyze_subtitle_text

        result = analyze_subtitle_text(episode.subtitle_content or episode.subtitle_url or "")
        if force_reanalyze:
            db.query(HighlightEvent).filter(HighlightEvent.episode_id == episode.id).delete()

        created: list[HighlightEvent] = []
        invalid_reasons: list[str] = []
        for item in result["highlights"]:
            try:
                highlight = create_highlight(db, episode, item)
            except ValueError as exc:
                invalid_reasons.append(str(exc))
                continue
            created.append(highlight)

        episode.analyze_status = "success"
        episode.analyze_error = "; ".join(invalid_reasons[:3])
        db.commit()
        return {
            "highlight_count": len(created),
            "provider": result.get("provider", "unknown"),
            "llm_error": result.get("llm_error", ""),
            "invalid_count": len(invalid_reasons),
        }
    except Exception as exc:
        episode.analyze_status = "failed"
        episode.analyze_error = str(exc)
        db.commit()
        raise
