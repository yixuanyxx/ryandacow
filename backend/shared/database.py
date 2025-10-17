import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Supabase URL and Service Key must be provided")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
    
    def get_client(self) -> Client:
        return self.client

# Global database connection instance
db_connection = DatabaseConnection()

def get_db_connection() -> Client:
    """Get Supabase client connection"""
    return db_connection.get_client()
