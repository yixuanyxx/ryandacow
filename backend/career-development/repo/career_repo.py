import sys
sys.path.append('..')
from shared.database import get_db_connection
from typing import Optional, Dict, Any, List

class CareerRepo:
    def __init__(self):
        self.db = get_db_connection()

    def get_all_pathways(self) -> List[Dict[str, Any]]:
        """Get all active career pathways"""
        res = self.db.table("career_pathways").select("*").eq("is_active", True).order("name").execute()
        return res.data or []

    def get_pathway_requirements(self, pathway_id: int) -> List[Dict[str, Any]]:
        """Get requirements for a career pathway"""
        res = self.db.table("pathway_requirements").select(`
            *,
            skills(*)
        `).eq("pathway_id", pathway_id).execute()
        return res.data or []
