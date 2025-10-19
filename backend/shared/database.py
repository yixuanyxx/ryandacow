import os
from typing import Optional

_db = None  # global singleton

class DatabaseConnection:
    def __init__(self):
        from supabase import create_client, Client

        self.demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
        self.supabase_url = os.getenv("SUPABASE_URL", "").strip()
        self.supabase_key = os.getenv("SUPABASE_SERVICE_KEY", "").strip()

        if self.demo_mode or not (self.supabase_url and self.supabase_key):
            self.client: Optional[Client] = None
        else:
            try:
                self.client: Client = create_client(self.supabase_url, self.supabase_key)
            except Exception as e:
                print(f"[WARN] Failed to init Supabase: {e}")
                self.client = None

    def ready(self) -> bool:
        return self.client is not None and not self.demo_mode


def get_db_connection() -> DatabaseConnection:
    global _db
    if _db is None:
        _db = DatabaseConnection()
    return _db