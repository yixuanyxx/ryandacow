import os
from typing import Optional, Dict, Any, List
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]

TABLE = "employee"

class EmployeeRepo:
    def __init__(self):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def insert_employee(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a new employee into the database."""
        res = self.client.table(TABLE).insert(data).execute()
        if not res.data:
            raise RuntimeError("Insert failed – no data returned")
        return res.data[0]

    def find_all(self) -> List[Dict[str, Any]]:
        """Find all employees, ordered by created_at descending."""
        res = self.client.table(TABLE).select("*").order("created_at", desc=True).execute()
        return res.data or []

    def get_employee(self, employee_id: int) -> Optional[Dict[str, Any]]:
        """Get a single employee by their ID."""
        res = self.client.table(TABLE).select("*").eq("id", employee_id).single().execute()
        return res.data

    def update_employee(self, employee_id: int, patch: Dict[str, Any]) -> Dict[str, Any]:
        """Update an employee with the provided fields."""
        res = self.client.table(TABLE).update(patch).eq("id", employee_id).execute()
        if not res.data:
            raise RuntimeError("Update failed – no data returned")
        return res.data[0]

    def delete_employee(self, employee_id: int) -> bool:
        """Delete an employee by their ID."""
        res = self.client.table(TABLE).delete().eq("id", employee_id).execute()
        return len(res.data) > 0
