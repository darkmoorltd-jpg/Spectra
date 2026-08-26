
import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime
import time

# Supabase setup
url = st.secrets["supabase"]["url"]
service_key = st.secrets["supabase"]["service_key"]
service = create_client(url, service_key)

st.set_page_config(page_title="Admin Dashboard", page_icon="🔐", layout="wide")
st.markdown("<style>header,footer{visibility:hidden}</style>", unsafe_allow_html=True)
st.title("🔐 SPECTRA Admin Dashboard")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in first.")
    st.stop()

# Only allow admin email (change to your admin email)
ADMIN_EMAIL = "darkmoorltd@gmail.com"
if st.session_state.user.email != ADMIN_EMAIL:
    st.error("Access denied. Admin only.")
    st.stop()

# ============================================
# Helper functions (using service role)
# ============================================
@st.cache_data(ttl=60)
def get_all_users():
    """Fetch all auth users and combine with profiles, scans, wallets, verifications."""
    users = []
    profiles = []
    scans = []
    wallets = []
    verifications = []

    # Get auth users via service role
    try:
        auth_users = service.auth.admin.list_users()
        if hasattr(auth_users, 'users'):
            users = auth_users.users
        elif isinstance(auth_users, list):
            users = auth_users
    except Exception as e:
        st.error(f"Failed to list auth users: {e}")
        return []

    # Get profiles
    try:
        p = service.table("user_profiles").select("*").execute()
        profiles = p.data if p.data else []
    except:
        profiles = []

    # Get scans
    try:
        s = service.table("user_scans").select("*").execute()
        scans = s.data if s.data else []
    except:
        scans = []

    # Get wallets
    try:
        w = service.table("farmer_wallets").select("*").execute()
        wallets = w.data if w.data else []
    except:
        wallets = []

    # Get verifications
    try:
        v = service.table("farmer_verifications").select("*").execute()
        verifications = v.data if v.data else []
    except:
        verifications = []

    # Build maps
    profile_map = {p["user_id"]: p for p in profiles if "user_id" in p}
    scan_map = {s["user_id"]: s for s in scans if "user_id" in s}
    wallet_map = {w["user_id"]: w for w in wallets if "user_id" in w}
    verify_map = {v["user_id"]: v for v in verifications if "user_id" in v}

    user_list = []
    for u in users:
        uid = u.id if hasattr(u, 'id') else u.get('id')
        if not uid:
            continue
        email = u.email if hasattr(u, 'email') else u.get('email', '')
        created = u.created_at if hasattr(u, 'created_at') else u.get('created_at', '')
        p = profile_map.get(uid, {})
        s = scan_map.get(uid, {})
        w = wallet_map.get(uid, {})
        v = verify_map.get(uid, {})
        user_list.append({
            "user_id": uid,
            "email": email or "N/A",
            "created_at": created or "",
            "scans_remaining": int(s.get("scans_remaining", 0)) if s.get("scans_remaining") is not None else 0,
            "plan": s.get("plan", "free"),
            "wallet_balance": float(w.get("balance", 0)) if w.get("balance") else 0,
            "verification_status": v.get("status", p.get("verification_status", "pending")),
            **p
        })
    return user_list

def add_scans(user_id, amount):
    """Add scans to user's account."""
    if amount <= 0:
        return False, "Amount must be positive"
    try:
        cur_res = service.table("user_scans").select("scans_remaining").eq("user_id", user_id).execute()
        cur = cur_res.data[0]["scans_remaining"] if cur_res.data else 0
        new_total = cur + amount
        service.table("user_scans").update({"scans_remaining": new_total}).eq("user_id", user_id).execute()
        return True, f"Added {amount} scans. New total: {new_total}"
    except Exception as e:
        return False, str(e)

def delete_user(user_id):
    """Delete a user and all related data."""
    tables = [
        "payment_history", "messages", "farmer_verifications", "user_profiles",
        "user_scans", "marketplace_listings", "marketplace_orders", "insurance_policies",
        "insurance_claims", "field_monitoring", "seller_profiles", "badge_subscriptions",
        "farmer_wallets", "pending_payments", "posts", "friendships", "chat_members",
        "user_status", "user_feedback", "scan_history", "user_streaks", "referrals",
        "mineral_buyers", "price_alerts", "find_of_day_submissions"
    ]
    for table in tables:
        try:
            service.table(table).delete().eq("user_id", user_id).execute()
        except:
            pass
    try:
        service.auth.admin.delete_user(user_id)
        return True, "User deleted successfully"
    except Exception as e:
        return False, f"Auth deletion failed: {e}"

def create_user(email, password, first_name="", last_name="", phone="", state=""):
    """Create a new user with profile and scans."""
    try:
        auth_res = service.auth.admin.create_user({
            "email": email,
            "password": password,
            "email_confirm": True
        })
        if auth_res.user:
            uid = auth_res.user.id
            service.table("user_profiles").insert({
                "user_id": uid, "first_name": first_name, "last_name": last_name,
                "phone": phone, "state": state, "verification_status": "pending"
            }).execute()
            service.table("user_scans").insert({
                "user_id": uid, "scans_remaining": 30, "plan": "free"
            }).execute()
            return True, f"User created with 30 free scans"
        else:
            return False, "User creation failed"
    except Exception as e:
        return False, str(e)

def update_kyc(user_id, status):
    """Update KYC status in both farmer_verifications and user_profiles."""
    try:
        service.table("farmer_verifications").update({"status": status}).eq("user_id", user_id).execute()
    except:
        pass
    try:
        service.table("user_profiles").update({"verification_status": status}).eq("user_id", user_id).execute()
    except:
        pass

def change_password(user_id, new_password):
    """Reset password for a user via admin API."""
    try:
        service.auth.admin.update_user_by_id(user_id, {"password": new_password})
        return True, "Password updated"
    except Exception as e:
        return False, str(e)

# ============================================
# Load all users
# ============================================
users = get_all_users()

# ============================================
# Tabs
# ============================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "👤 All Users", "🛡️ KYC Queue", "➕ Create User", "💳 Payment History"])

# ----- Overview -----
with tab1:
    total = len(users)
    verified = sum(1 for u in users if u.get("verification_status") == "approved")
    pending = sum(1 for u in users if u.get("verification_status") == "pending")
    rejected = sum(1 for u in users if u.get("verification_status") == "rejected")
    paid = sum(1 for u in users if u.get("plan", "free") != "free")

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Users", total)
    col2.metric("Verified", verified)
    col3.metric("Pending KYC", pending)
    col4.metric("Rejected", rejected)
    col5.metric("Paid Plans", paid)

    if users:
        summary = []
        for u in users:
            summary.append({
                "Email": u.get("email"),
                "Name": f"{u.get('first_name','')} {u.get('last_name','')}".strip(),
                "Phone": u.get("phone", ""),
                "State": u.get("state", ""),
                "KYC": u.get("verification_status", "pending"),
                "Scans": u.get("scans_remaining", 0),
                "Plan": u.get("plan", "free"),
                "Wallet": f"₦{u.get('wallet_balance', 0):,.2f}",
                "Joined": str(u.get("created_at", ""))[:10],
            })
        st.dataframe(pd.DataFrame(summary), use_container_width=True)
    else:
        st.info("No users found.")

# ----- All Users -----
with tab2:
    if not users:
        st.info("No users.")
    else:
        emails = [u.get("email") for u in users]
        selected_email = st.selectbox("Select User", emails, key="admin_all_users")
        user = next((u for u in users if u.get("email") == selected_email), None)
        if user:
            user_id = user["user_id"]
            st.markdown(f"### 👤 {user.get('first_name','')} {user.get('last_name','')}")
            st.write(f"**Email:** {user.get('email')}")
            st.write(f"**User ID:** {user_id}")
            st.write(f"**Joined:** {str(user.get('created_at',''))[:10]}")
            st.write(f"**Phone:** {user.get('phone','N/A')}")
            st.write(f"**WhatsApp:** {user.get('whatsapp','N/A')}")

            # -------------------------------------------------
            # FULL PROFILE DISPLAY
            # -------------------------------------------------
            st.markdown("---")
            st.subheader("📋 Full Profile Information")

            # Personal Information
            with st.expander("👤 Personal Information", expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"First Name: {user.get('first_name','')}")
                    st.write(f"Middle Name: {user.get('middle_name','')}")
                    st.write(f"Last Name: {user.get('last_name','')}")
                    st.write(f"Gender: {user.get('gender','')}")
                with col2:
                    st.write(f"Date of Birth: {str(user.get('date_of_birth',''))[:10]}")
                    st.write(f"Marital Status: {user.get('marital_status','')}")
                    st.write(f"Phone: {user.get('phone','')}")
                    st.write(f"WhatsApp: {user.get('whatsapp','')}")
                with col3:
                    st.write(f"Country: {user.get('country','')}")
                    st.write(f"State: {user.get('state','')}")
                    st.write(f"LGA: {user.get('lga','')}")
                    st.write(f"City: {user.get('city','')}")
                    st.write(f"Street: {user.get('street_address','')}")
                    st.write(f"Landmark: {user.get('landmark','')}")
                    st.write(f"Postal Code: {user.get('postal_code','')}")

            # KYC Information
            with st.expander("🛡️ KYC Information", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"BVN: {user.get('bvn','')}")
                    st.write(f"NIN: {user.get('nin','')}")
                    st.write(f"Govt ID Type: {user.get('govt_id_type','')}")
                    st.write(f"Govt ID Number: {user.get('govt_id_number','')}")
                with col2:
                    st.write(f"Verification Status: {user.get('verification_status','pending')}")

            # Mining Information
            with st.expander("⛏️ Mining Information", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"Mining State: {user.get('mining_state','')}")
                    st.write(f"Mining LGA: {user.get('mining_lga','')}")
                    st.write(f"Mining Address: {user.get('mining_address','')}")
                with col2:
                    st.write(f"Minerals of Interest: {user.get('minerals_of_interest','')}")
                    st.write(f"Years Experience: {user.get('years_mining_experience',0)}")
                    st.write(f"License Number: {user.get('mining_license_number','')}")
                with col3:
                    st.write(f"Cooperative: {user.get('mining_cooperative','')}")
                    st.write(f"Mining Type: {user.get('mining_type','')}")

            # Bank Information
            with st.expander("🏦 Bank Information", expanded=False):
                st.write(f"Account Name: {user.get('account_name','')}")
                st.write(f"Account Number: {user.get('account_number','')}")
                st.write(f"Bank Name: {user.get('bank_name','')}")

            # Emergency Contact
            with st.expander("🚨 Emergency Contact", expanded=False):
                st.write(f"Name: {user.get('emergency_contact_name','')}")
                st.write(f"Phone: {user.get('emergency_contact_phone','')}")
                st.write(f"Relationship: {user.get('emergency_relationship','')}")

            # Notifications
            with st.expander("🔔 Notification Preferences", expanded=False):
                st.write(f"SMS: {user.get('notify_sms', True)}")
                st.write(f"WhatsApp: {user.get('notify_whatsapp', True)}")
                st.write(f"Weather: {user.get('notify_weather', True)}")
                st.write(f"Disease: {user.get('notify_disease', True)}")
                st.write(f"Payment: {user.get('notify_payment', True)}")
                st.write(f"Language: {user.get('preferred_language','English')}")

            # Account status (scans, plan, wallet)
            st.markdown("---")
            st.write(f"**Scans Remaining:** {user.get('scans_remaining',0)}")
            st.write(f"**Plan:** {user.get('plan','free')}")
            st.write(f"**Wallet Balance:** ₦{user.get('wallet_balance',0):,.2f}")

            # -------------------------------------------------
            # ACTIONS
            # -------------------------------------------------
            st.markdown("---")
            st.subheader("⚙️ Actions")

            # Add scans
            with st.form(f"add_scans_{user_id}"):
                add_amount = st.number_input("Scans to add", min_value=1, value=1)
                if st.form_submit_button("➕ Add Scans"):
                    ok, msg = add_scans(user_id, add_amount)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

            # Change password
            with st.form(f"change_pass_{user_id}"):
                new_pass = st.text_input("New Password", type="password")
                if st.form_submit_button("🔑 Reset Password"):
                    if new_pass:
                        ok, msg = change_password(user_id, new_pass)
                        if ok:
                            st.success(msg)
                        else:
                            st.error(msg)
                    else:
                        st.warning("Enter a new password")

            # KYC actions
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Approve KYC", key=f"approve_{user_id}"):
                    update_kyc(user_id, "approved")
                    st.success("KYC approved")
                    st.rerun()
            with col2:
                if st.button("❌ Reject KYC", key=f"reject_{user_id}"):
                    update_kyc(user_id, "rejected")
                    st.success("KYC rejected")
                    st.rerun()

            # Delete user
            with st.expander("🗑️ Danger Zone"):
                st.warning("This permanently deletes the user and all data.")
                confirm = st.checkbox("I understand", key=f"confirm_{user_id}")
                if st.button("Delete User", key=f"del_{user_id}") and confirm:
                    ok, msg = delete_user(user_id)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

# ----- KYC Queue -----
with tab3:
    st.markdown("### 🛡️ Pending KYC")
    pending_users = [u for u in users if u.get("verification_status") == "pending"]
    if not pending_users:
        st.info("No pending KYC.")
    else:
        for u in pending_users:
            with st.expander(f"⏳ {u.get('first_name')} {u.get('last_name')} — {u.get('email')}"):
                st.write(f"BVN: {u.get('bvn','N/A')}")
                st.write(f"NIN: {u.get('nin','N/A')}")
                st.write(f"ID Type: {u.get('govt_id_type','N/A')}")
                st.write(f"ID Number: {u.get('govt_id_number','N/A')}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Approve", key=f"app_{u['user_id']}"):
                        update_kyc(u["user_id"], "approved")
                        st.success("Approved")
                        st.rerun()
                with col2:
                    if st.button("❌ Reject", key=f"rej_{u['user_id']}"):
                        update_kyc(u["user_id"], "rejected")
                        st.success("Rejected")
                        st.rerun()

# ----- Create User -----
with tab4:
    st.markdown("### ➕ Create New User")
    with st.form("create_user_form"):
        col1, col2 = st.columns(2)
        with col1:
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            new_first = st.text_input("First Name")
        with col2:
            new_last = st.text_input("Last Name")
            new_phone = st.text_input("Phone")
            new_state = st.text_input("State")
        if st.form_submit_button("➕ Create User"):
            if not new_email or not new_password:
                st.error("Email and password required.")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                ok, msg = create_user(new_email, new_password, new_first, new_last, new_phone, new_state)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

# ----- Payment History -----
with tab5:
    st.markdown("### 💳 Payment History (All Users)")
    try:
        payments = service.table("payment_history").select("*").order("paid_at", desc=True).limit(200).execute()
        if payments.data:
            df = pd.DataFrame(payments.data)
            user_emails = {u["user_id"]: u["email"] for u in users}
            df["email"] = df["user_id"].map(user_emails)
            df["paid_at"] = pd.to_datetime(df["paid_at"]).dt.strftime("%Y-%m-%d %H:%M")
            df = df[["email", "amount", "scans_added", "plan", "reference", "paid_at"]]
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No payments recorded.")
    except Exception as e:
        st.error(f"Failed to load payments: {e}")
