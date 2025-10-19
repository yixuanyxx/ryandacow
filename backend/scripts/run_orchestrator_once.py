from backend.ai_chat.orchestrator.orchestrator import run_full_plan
import json

print(json.dumps(run_full_plan(1), indent=2))