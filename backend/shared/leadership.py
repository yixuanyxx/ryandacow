# backend/shared/leadership.py

from typing import Dict, List

def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))

def leadership_score(signals: Dict) -> Dict:
    """
    Compute a transparent leadership readiness score.
    signals keys (defaults if missing):
      - training_completion: 0..1
      - recognition_count: int (we cap effect at 5)
      - engagement: 0..1
      - positive_feedback_ratio: 0..1
    """
    training = float(signals.get("training_completion", 0.0))
    recog    = float(signals.get("recognition_count", 0))
    engage   = float(signals.get("engagement", 0.0))
    posfb    = float(signals.get("positive_feedback_ratio", 0.0))

    score_raw = (
        0.35 * training +
        0.25 * _clamp(recog / 5.0) +
        0.20 * engage +
        0.20 * posfb
    )
    score = round(100.0 * _clamp(score_raw), 1)

    if score >= 75:
        level = "Ready"
    elif score >= 50:
        level = "Developing"
    else:
        level = "Early"

    rationale: List[str] = []
    rationale.append("Strong training momentum" if training > 0.6 else "Increase consistent upskilling cadence")
    rationale.append("Peer recognition trending well" if recog >= 3 else "Seek visibility via cross-team contributions")
    rationale.append("Healthy engagement" if engage > 0.6 else "Boost engagement through mentoring or guilds")
    rationale.append("Positive feedback pattern" if posfb > 0.6 else "Request frequent feedback and track improvements")

    # A minimal, actionable plan the UI can render
    plan = [
        {"skill": "Stakeholder & Partnership Management", "priority": "High", "timeline": "6–8 weeks"},
        {"skill": "Systems Thinking", "priority": "High", "timeline": "8–10 weeks"},
        {"skill": "Coaching & Feedback", "priority": "Medium", "timeline": "4–6 weeks"},
    ]

    return {
        "score": score,
        "level": level,
        "rationale": rationale,
        "development_plan": plan
    }