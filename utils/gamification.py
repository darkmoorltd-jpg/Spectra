
import streamlit as st
from supabase import create_client

def get_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def update_streak(user_id):
    """Update daily streak and return current streak count."""
    client = get_supabase()
    # In production, use a table streak_tracking with last_scan_date and streak_count
    # For now, simulate with a simple table (create via SQL later)
    try:
        res = client.table("user_streaks").select("*").eq("user_id", user_id).execute()
        if res.data:
            streak = res.data[0].get("streak_count", 0)
            last_date = res.data[0].get("last_scan_date")
            today = str(datetime.date.today())
            if last_date == today:
                return streak
            elif last_date == str(datetime.date.today() - datetime.timedelta(days=1)):
                streak += 1
            else:
                streak = 1
            client.table("user_streaks").update({"streak_count": streak, "last_scan_date": today}).eq("user_id", user_id).execute()
            return streak
        else:
            client.table("user_streaks").insert({"user_id": user_id, "streak_count": 1, "last_scan_date": str(datetime.date.today())}).execute()
            return 1
    except:
        return 1

def get_leaderboard(limit=10):
    """Return top miners by total scans (requires table scan_history)."""
    client = get_supabase()
    try:
        res = client.table("scan_history").select("user_id, count").execute()
        # Group by user_id, sum count; simplified: assume each row is one scan
        # In real implementation, use a view or aggregate query
        # We'll just return dummy data for now
        return []
    except:
        return []
