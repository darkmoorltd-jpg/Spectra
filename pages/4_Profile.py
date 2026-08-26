from utils.sidebar import render_sidebar

import streamlit as st
from supabase import create_client
import datetime

# Supabase setup
url = st.secrets["supabase"]["url"]
service_key = st.secrets["supabase"]["service_key"]
service = create_client(url, service_key)

st.set_page_config(page_title="My Profile", page_icon="👤", layout="wide")
render_sidebar()
st.markdown("<style>header,footer{visibility:hidden}</style>", unsafe_allow_html=True)
st.title("👤 My Profile")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in first.")
    st.stop()

user = st.session_state.user
user_id = user.id

# Load existing profile using service client
try:
    res = service.table("user_profiles").select("*").eq("user_id", user_id).execute()
    profile = res.data[0] if res.data else None
except Exception as e:
    st.error(f"Could not load profile: {e}")
    profile = None

# Helper to get value from profile or default
def get_val(key, default=""):
    if profile and key in profile:
        return profile[key]
    return default

with st.form("profile_form"):
    st.markdown("## 📋 Personal Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        first_name = st.text_input("First Name *", value=get_val("first_name"))
        middle_name = st.text_input("Middle Name", value=get_val("middle_name"))
        gender = st.selectbox("Gender", ["", "Male", "Female"], index=0 if not get_val("gender") else ["", "Male", "Female"].index(get_val("gender")))
    with col2:
        last_name = st.text_input("Last Name *", value=get_val("last_name"))
        date_of_birth = st.date_input("Date of Birth", value=None if not get_val("date_of_birth") else datetime.date.fromisoformat(str(get_val("date_of_birth"))), key="dob")
        marital_status = st.selectbox("Marital Status", ["", "Single", "Married", "Divorced", "Widowed"], index=0 if not get_val("marital_status") else ["", "Single", "Married", "Divorced", "Widowed"].index(get_val("marital_status")))
    with col3:
        phone = st.text_input("Phone *", value=get_val("phone"))
        whatsapp = st.text_input("WhatsApp", value=get_val("whatsapp"))
        email = st.text_input("Email", value=user.email, disabled=True)

    st.markdown("---")
    st.markdown("## 🏠 Address")
    col1, col2, col3 = st.columns(3)
    with col1:
        country = st.text_input("Country", value=get_val("country", "Nigeria"))
        state = st.text_input("State", value=get_val("state"))
        lga = st.text_input("LGA", value=get_val("lga"))
    with col2:
        city = st.text_input("City/Town", value=get_val("city"))
        street_address = st.text_input("Street Address", value=get_val("street_address"))
        landmark = st.text_input("Landmark", value=get_val("landmark"))
    with col3:
        postal_code = st.text_input("Postal Code", value=get_val("postal_code"))

    st.markdown("---")
    st.markdown("## 🛡️ KYC Information")
    col1, col2 = st.columns(2)
    with col1:
        bvn = st.text_input("BVN (11 digits)", value=get_val("bvn"), max_chars=11)
        nin = st.text_input("NIN (11 digits)", value=get_val("nin"), max_chars=11)
        govt_id_type = st.selectbox("Government ID Type", ["", "National ID Card", "Driver's License", "International Passport", "Voter's Card (PVC)", "NIN Slip"], index=0 if not get_val("govt_id_type") else ["", "National ID Card", "Driver's License", "International Passport", "Voter's Card (PVC)", "NIN Slip"].index(get_val("govt_id_type")))
    with col2:
        govt_id_number = st.text_input("ID Number", value=get_val("govt_id_number"))

    st.markdown("---")
    st.markdown("## ⛏️ Mining Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        mining_state = st.text_input("Mining State", value=get_val("mining_state"))
        mining_lga = st.text_input("Mining LGA", value=get_val("mining_lga"))
        mining_address = st.text_input("Mining Address", value=get_val("mining_address"))
    with col2:
        minerals_of_interest = st.text_input("Minerals of Interest", value=get_val("minerals_of_interest"))
        years_mining_experience = st.number_input("Years of Mining Experience", min_value=0, value=int(get_val("years_mining_experience", 0)))
        mining_license_number = st.text_input("Mining License Number", value=get_val("mining_license_number"))
    with col3:
        mining_cooperative = st.text_input("Mining Cooperative", value=get_val("mining_cooperative"))
        mining_type = st.selectbox("Mining Type", ["", "Artisanal", "Small-scale", "Medium-scale", "Large-scale"], index=0 if not get_val("mining_type") else ["", "Artisanal", "Small-scale", "Medium-scale", "Large-scale"].index(get_val("mining_type")))

    st.markdown("---")
    st.markdown("## 🏦 Bank Information")
    col1, col2 = st.columns(2)
    with col1:
        account_name = st.text_input("Account Name", value=get_val("account_name"))
        bank_name = st.selectbox("Bank", ["", "Access Bank", "GTBank", "Zenith Bank", "UBA", "First Bank", "Kuda", "Opay", "Palmpay", "Moniepoint", "Sterling Bank", "Union Bank", "Fidelity Bank", "Wema Bank"], index=0 if not get_val("bank_name") else ["", "Access Bank", "GTBank", "Zenith Bank", "UBA", "First Bank", "Kuda", "Opay", "Palmpay", "Moniepoint", "Sterling Bank", "Union Bank", "Fidelity Bank", "Wema Bank"].index(get_val("bank_name")))
    with col2:
        account_number = st.text_input("Account Number", value=get_val("account_number"), max_chars=10)

    st.markdown("---")
    st.markdown("## 🚨 Emergency Contact")
    col1, col2 = st.columns(2)
    with col1:
        emergency_name = st.text_input("Contact Name", value=get_val("emergency_contact_name"))
        emergency_relationship = st.text_input("Relationship", value=get_val("emergency_relationship"))
    with col2:
        emergency_phone = st.text_input("Contact Phone", value=get_val("emergency_contact_phone"))

    st.markdown("---")
    st.markdown("## 🔔 Notification Preferences")
    col1, col2 = st.columns(2)
    with col1:
        notify_sms = st.checkbox("SMS Notifications", value=bool(get_val("notify_sms", True)))
        notify_whatsapp = st.checkbox("WhatsApp", value=bool(get_val("notify_whatsapp", True)))
        notify_weather = st.checkbox("Weather Alerts", value=bool(get_val("notify_weather", True)))
    with col2:
        notify_disease = st.checkbox("Disease Alerts", value=bool(get_val("notify_disease", True)))
        notify_payment = st.checkbox("Payment Alerts", value=bool(get_val("notify_payment", True)))
        preferred_language = st.selectbox("Preferred Language", ["English", "Hausa", "Yoruba", "Igbo", "Pidgin English"], index=0 if not get_val("preferred_language") else ["English", "Hausa", "Yoruba", "Igbo", "Pidgin English"].index(get_val("preferred_language")))

    submitted = st.form_submit_button("💾 Save Profile & Lock", type="primary", use_container_width=True)

if submitted:
    if not first_name or not last_name or not phone:
        st.error("❌ First name, last name, and phone are required.")
    else:
        update_data = {
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "middle_name": middle_name.strip() if middle_name else None,
            "phone": phone.strip(),
            "whatsapp": whatsapp.strip() if whatsapp else None,
            "gender": gender if gender else None,
            "marital_status": marital_status if marital_status else None,
            "country": country.strip() or "Nigeria",
            "state": state.strip() if state else None,
            "lga": lga.strip() if lga else None,
            "city": city.strip() if city else None,
            "street_address": street_address.strip() if street_address else None,
            "landmark": landmark.strip() if landmark else None,
            "postal_code": postal_code.strip() if postal_code else None,
            "bvn": bvn.strip() if bvn else None,
            "nin": nin.strip() if nin else None,
            "govt_id_type": govt_id_type if govt_id_type else None,
            "govt_id_number": govt_id_number.strip() if govt_id_number else None,
            "mining_state": mining_state.strip() if mining_state else None,
            "mining_lga": mining_lga.strip() if mining_lga else None,
            "mining_address": mining_address.strip() if mining_address else None,
            "minerals_of_interest": minerals_of_interest.strip() if minerals_of_interest else None,
            "years_mining_experience": years_mining_experience,
            "mining_license_number": mining_license_number.strip() if mining_license_number else None,
            "mining_cooperative": mining_cooperative.strip() if mining_cooperative else None,
            "mining_type": mining_type if mining_type else None,
            "account_name": account_name.strip() if account_name else None,
            "account_number": account_number.strip() if account_number else None,
            "bank_name": bank_name if bank_name else None,
            "emergency_contact_name": emergency_name.strip() if emergency_name else None,
            "emergency_contact_phone": emergency_phone.strip() if emergency_phone else None,
            "emergency_relationship": emergency_relationship.strip() if emergency_relationship else None,
            "notify_sms": notify_sms,
            "notify_whatsapp": notify_whatsapp,
            "notify_weather": notify_weather,
            "notify_disease": notify_disease,
            "notify_payment": notify_payment,
            "preferred_language": preferred_language,
            "verification_status": "pending" if not profile else profile.get("verification_status", "pending"),
        }
        if date_of_birth:
            update_data["date_of_birth"] = date_of_birth.isoformat()

        try:
            if profile:
                service.table("user_profiles").update(update_data).eq("user_id", user_id).execute()
            else:
                update_data["user_id"] = user_id
                service.table("user_profiles").insert(update_data).execute()
            st.success("✅ Profile saved successfully! Your information is now pinned to your account.")
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"Error saving profile: {e}")