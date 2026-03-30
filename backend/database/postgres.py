from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def create_user(username: str, email: str) -> dict:
    result = supabase.table("users").insert({
        "username": username,
        "email": email
    }).execute()
    return result.data[0]


def get_user(user_id: str) -> dict | None:
    result = supabase.table("users").select("*").eq("id", user_id).execute()
    if result.data:
        return result.data[0]
    return None


def get_user_by_email(email: str) -> dict | None:
    result = supabase.table("users").select("*").eq("email", email).execute()
    if result.data:
        return result.data[0]
    return None


def list_users() -> list[dict]:
    result = supabase.table("users").select("*").order("created_at", desc=True).execute()
    return result.data
