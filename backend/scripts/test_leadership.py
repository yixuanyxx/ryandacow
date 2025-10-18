from backend.shared.leadership import leadership_score
import json

# Example signals (mocked). Later you can compute these per user.
signals = {
    "training_completion": 0.55,
    "recognition_count": 2,
    "engagement": 0.7,
    "positive_feedback_ratio": 0.65
}

print(json.dumps(leadership_score(signals), indent=2))