
import streamlit as st
from supabase import create_client
import datetime

# Supabase setup
url = st.secrets["supabase"]["url"]
service_key = st.secrets["supabase"]["service_key"]
service = create_client(url, service_key)

st.set_page_config(page_title="My Profile", page_icon="👤", layout="wide")
st.markdown("<style>header,footer{visibility:hidden}</style>", unsafe_allow_html=True)
st.title("👤 My Profile")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in first.")
    st.stop()

user = st.session_state.user
user_id = user.id

# Load existing profile
try:
    res = service.table("user_profiles").select("*").eq("user_id", user_id).execute()
    profile = res.data[0] if res.data else None
except Exception as e:
    st.error(f"Could not load profile: {e}")
    profile = None

def get_val(key, default=""):
    if profile and key in profile:
        return profile[key]
    return default

# Full list of countries
COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain",
    "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
    "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada",
    "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros",
    "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus",
    "Czechia (Czech Republic)", "Democratic Republic of the Congo", "Denmark", "Djibouti",
    "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea",
    "Eritrea", "Estonia", "Eswatini (Swaziland)", "Ethiopia", "Fiji", "Finland", "France",
    "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala",
    "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland",
    "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast",
    "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait",
    "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya",
    "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia",
    "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius",
    "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco",
    "Mozambique", "Myanmar (Burma)", "Namibia", "Nauru", "Nepal", "Netherlands",
    "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia",
    "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea",
    "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania",
    "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines",
    "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia",
    "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands",
    "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka",
    "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan",
    "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago",
    "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates",
    "United Kingdom", "United States of America", "Uruguay", "Uzbekistan", "Vanuatu",
    "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]

with st.form("profile_form"):
    st.markdown("## 📋 Personal Information (All fields required except Middle Name)")
    col1, col2, col3 = st.columns(3)
    with col1:
        first_name = st.text_input("First Name *", value=get_val("first_name"))
        middle_name = st.text_input("Middle Name (Optional)", value=get_val("middle_name"))
        gender = st.selectbox("Gender *", ["", "Male", "Female"], index=0 if not get_val("gender") else ["", "Male", "Female"].index(get_val("gender")))
    with col2:
        last_name = st.text_input("Last Name *", value=get_val("last_name"))
        date_of_birth = st.date_input("Date of Birth *", value=None if not get_val("date_of_birth") else datetime.date.fromisoformat(str(get_val("date_of_birth"))))
        marital_status = st.selectbox("Marital Status *", ["", "Single", "Married", "Divorced", "Widowed"], index=0 if not get_val("marital_status") else ["", "Single", "Married", "Divorced", "Widowed"].index(get_val("marital_status")))
    with col3:
        phone = st.text_input("Phone *", value=get_val("phone"))
        whatsapp = st.text_input("WhatsApp *", value=get_val("whatsapp"))
        email = st.text_input("Email", value=user.email, disabled=True)

    st.markdown("---")
    st.markdown("## 🏠 Address")
    col1, col2, col3 = st.columns(3)
    with col1:
        country = st.selectbox("Country *", COUNTRIES, index=COUNTRIES.index(get_val("country", "Nigeria")) if get_val("country", "Nigeria") in COUNTRIES else COUNTRIES.index("Nigeria"))
        state = st.text_input("State *", value=get_val("state"))
        lga = st.text_input("LGA *", value=get_val("lga"))
    with col2:
        city = st.text_input("City/Town *", value=get_val("city"))
        street_address = st.text_input("Street Address *", value=get_val("street_address"))
        landmark = st.text_input("Landmark *", value=get_val("landmark"))
    with col3:
        postal_code = st.text_input("Postal Code *", value=get_val("postal_code"))

    st.markdown("---")
    st.markdown("## 🛡️ KYC Information")
    col1, col2 = st.columns(2)
    with col1:
        bvn = st.text_input("BVN (11 digits) *", value=get_val("bvn"), max_chars=11)
        nin = st.text_input("NIN (11 digits) *", value=get_val("nin"), max_chars=11)
        govt_id_type = st.selectbox("Government ID Type *", ["", "National ID Card", "Driver's License", "International Passport", "Voter's Card (PVC)", "NIN Slip"], index=0 if not get_val("govt_id_type") else ["", "National ID Card", "Driver's License", "International Passport", "Voter's Card (PVC)", "NIN Slip"].index(get_val("govt_id_type")))
    with col2:
        govt_id_number = st.text_input("ID Number *", value=get_val("govt_id_number"))

    st.markdown("---")
    st.markdown("## ⛏️ Mining Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        mining_state = st.text_input("Mining State *", value=get_val("mining_state"))
        mining_lga = st.text_input("Mining LGA *", value=get_val("mining_lga"))
        mining_address = st.text_input("Mining Address *", value=get_val("mining_address"))
    with col2:
        minerals_of_interest = st.text_input("Minerals of Interest *", value=get_val("minerals_of_interest"))
        years_mining_experience = st.number_input("Years of Mining Experience *", min_value=0, value=int(get_val("years_mining_experience", 0)))
        mining_license_number = st.text_input("Mining License Number *", value=get_val("mining_license_number"))
    with col3:
        mining_cooperative = st.text_input("Mining Cooperative *", value=get_val("mining_cooperative"))
        mining_type = st.selectbox("Mining Type *", ["", "Artisanal", "Small-scale", "Medium-scale", "Large-scale"], index=0 if not get_val("mining_type") else ["", "Artisanal", "Small-scale", "Medium-scale", "Large-scale"].index(get_val("mining_type")))

    st.markdown("---")
    st.markdown("## 🏦 Bank Information")
    col1, col2 = st.columns(2)
    with col1:
        account_name = st.text_input("Account Name *", value=get_val("account_name"))
        bank_name = st.selectbox("Bank *", ["", "Access Bank", "GTBank", "Zenith Bank", "UBA", "First Bank", "Kuda", "Opay", "Palmpay", "Moniepoint", "Sterling Bank", "Union Bank", "Fidelity Bank", "Wema Bank"], index=0 if not get_val("bank_name") else ["", "Access Bank", "GTBank", "Zenith Bank", "UBA", "First Bank", "Kuda", "Opay", "Palmpay", "Moniepoint", "Sterling Bank", "Union Bank", "Fidelity Bank", "Wema Bank"].index(get_val("bank_name")))
    with col2:
        account_number = st.text_input("Account Number *", value=get_val("account_number"), max_chars=10)

    st.markdown("---")
    st.markdown("## 🚨 Emergency Contact")
    col1, col2 = st.columns(2)
    with col1:
        emergency_name = st.text_input("Contact Name *", value=get_val("emergency_contact_name"))
        emergency_relationship = st.text_input("Relationship *", value=get_val("emergency_relationship"))
    with col2:
        emergency_phone = st.text_input("Contact Phone *", value=get_val("emergency_contact_phone"))

    st.markdown("---")
    submitted = st.form_submit_button("💾 Save Profile", type="primary", use_container_width=True)

if submitted:
    # Validate all required fields except middle_name
    required_fields = {
        "First Name": first_name,
        "Last Name": last_name,
        "Gender": gender,
        "Date of Birth": date_of_birth,
        "Marital Status": marital_status,
        "Phone": phone,
        "WhatsApp": whatsapp,
        "Country": country,
        "State": state,
        "LGA": lga,
        "City": city,
        "Street Address": street_address,
        "Landmark": landmark,
        "Postal Code": postal_code,
        "BVN": bvn,
        "NIN": nin,
        "Government ID Type": govt_id_type,
        "ID Number": govt_id_number,
        "Mining State": mining_state,
        "Mining LGA": mining_lga,
        "Mining Address": mining_address,
        "Minerals of Interest": minerals_of_interest,
        "Years of Experience": years_mining_experience,
        "Mining License Number": mining_license_number,
        "Mining Cooperative": mining_cooperative,
        "Mining Type": mining_type,
        "Account Name": account_name,
        "Account Number": account_number,
        "Bank Name": bank_name,
        "Emergency Contact Name": emergency_name,
        "Emergency Contact Phone": emergency_phone,
        "Emergency Relationship": emergency_relationship,
    }
    
    missing = [k for k, v in required_fields.items() if not v]
    if missing:
        st.error(f"❌ Please fill all required fields: {', '.join(missing)}")
    else:
        update_data = {
            "first_name": first_name.strip(),
            "middle_name": middle_name.strip() if middle_name else None,
            "last_name": last_name.strip(),
            "gender": gender,
            "date_of_birth": date_of_birth.isoformat() if date_of_birth else None,
            "marital_status": marital_status,
            "phone": phone.strip(),
            "whatsapp": whatsapp.strip(),
            "country": country,
            "state": state.strip(),
            "lga": lga.strip(),
            "city": city.strip(),
            "street_address": street_address.strip(),
            "landmark": landmark.strip(),
            "postal_code": postal_code.strip(),
            "bvn": bvn.strip(),
            "nin": nin.strip(),
            "govt_id_type": govt_id_type,
            "govt_id_number": govt_id_number.strip(),
            "mining_state": mining_state.strip(),
            "mining_lga": mining_lga.strip(),
            "mining_address": mining_address.strip(),
            "minerals_of_interest": minerals_of_interest.strip(),
            "years_mining_experience": years_mining_experience,
            "mining_license_number": mining_license_number.strip(),
            "mining_cooperative": mining_cooperative.strip(),
            "mining_type": mining_type,
            "account_name": account_name.strip(),
            "account_number": account_number.strip(),
            "bank_name": bank_name,
            "emergency_contact_name": emergency_name.strip(),
            "emergency_contact_phone": emergency_phone.strip(),
            "emergency_relationship": emergency_relationship.strip(),
            "verification_status": profile.get("verification_status", "pending") if profile else "pending",
        }
        
        try:
            if profile:
                service.table("user_profiles").update(update_data).eq("user_id", user_id).execute()
            else:
                update_data["user_id"] = user_id
                service.table("user_profiles").insert(update_data).execute()
            st.success("✅ Profile saved successfully!")
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"Error saving profile: {e}")
