
import streamlit as st
from supabase import create_client
import datetime

st.set_page_config(page_title="Create Account – SPECTRA", page_icon="⛏️", layout="wide")

# Dark theme
st.markdown("""
<style>
    .stApp { background: radial-gradient(ellipse at 20% 50%, #0d1b2a 0%, #0a0e17 70%); color: #e0e0e0; }
    header, footer { visibility: hidden; }
    .title { font-size: 2.5rem; font-weight: 800; text-align: center; color: #ffd700; }
    .subtitle { text-align: center; color: #8892b0; margin-bottom: 2rem; }
    .stButton > button { background: #ffd700; color: #0a0e17; font-weight: bold; border: none; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">⛏️ Create SPECTRA Account</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Join the mining revolution – all fields required except Middle Name</div>', unsafe_allow_html=True)

# Supabase clients
url = st.secrets["supabase"]["url"]
anon_key = st.secrets["supabase"]["key"]
service_key = st.secrets["supabase"]["service_key"]
supabase = create_client(url, anon_key)
service = create_client(url, service_key)

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

with st.form("signup_form"):
    st.markdown("### 🔐 Account Credentials")
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email *")
        password = st.text_input("Password *", type="password", min_chars=6)
    with col2:
        confirm_password = st.text_input("Confirm Password *", type="password")

    st.markdown("---")
    st.markdown("### 📋 Personal Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        first_name = st.text_input("First Name *")
        middle_name = st.text_input("Middle Name (Optional)")
        gender = st.selectbox("Gender *", ["", "Male", "Female"])
    with col2:
        last_name = st.text_input("Last Name *")
        date_of_birth = st.date_input("Date of Birth *", min_value=datetime.date(1940, 1, 1), max_value=datetime.date.today())
        marital_status = st.selectbox("Marital Status *", ["", "Single", "Married", "Divorced", "Widowed"])
    with col3:
        phone = st.text_input("Phone *", placeholder="08031234567")
        whatsapp = st.text_input("WhatsApp *", placeholder="08031234567")

    st.markdown("---")
    st.markdown("### 🏠 Address")
    col1, col2, col3 = st.columns(3)
    with col1:
        country = st.selectbox("Country *", COUNTRIES, index=COUNTRIES.index("Nigeria"))
        state = st.text_input("State *")
        lga = st.text_input("LGA *")
    with col2:
        city = st.text_input("City/Town *")
        street_address = st.text_input("Street Address *")
        landmark = st.text_input("Landmark *")
    with col3:
        postal_code = st.text_input("Postal Code *")

    st.markdown("---")
    st.markdown("### 🛡️ KYC Information")
    col1, col2 = st.columns(2)
    with col1:
        bvn = st.text_input("BVN (11 digits) *", max_chars=11)
        nin = st.text_input("NIN (11 digits) *", max_chars=11)
        govt_id_type = st.selectbox("Government ID Type *", ["", "National ID Card", "Driver's License", "International Passport", "Voter's Card (PVC)", "NIN Slip"])
    with col2:
        govt_id_number = st.text_input("ID Number *")

    st.markdown("---")
    st.markdown("### ⛏️ Mining Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        mining_state = st.text_input("Mining State *")
        mining_lga = st.text_input("Mining LGA *")
        mining_address = st.text_input("Mining Address *")
    with col2:
        minerals_of_interest = st.text_input("Minerals of Interest *", placeholder="Gold, Lithium, Coltan")
        years_mining_experience = st.number_input("Years of Mining Experience *", min_value=0, value=0)
        mining_license_number = st.text_input("Mining License Number *", placeholder="N/A if none")
    with col3:
        mining_cooperative = st.text_input("Mining Cooperative *", placeholder="N/A if none")
        mining_type = st.selectbox("Mining Type *", ["", "Artisanal", "Small-scale", "Medium-scale", "Large-scale"])

    st.markdown("---")
    st.markdown("### 🏦 Bank Information")
    col1, col2 = st.columns(2)
    with col1:
        account_name = st.text_input("Account Name *")
        bank_name = st.selectbox("Bank *", ["", "Access Bank", "GTBank", "Zenith Bank", "UBA", "First Bank", "Kuda", "Opay", "Palmpay", "Moniepoint", "Sterling Bank", "Union Bank", "Fidelity Bank", "Wema Bank"])
    with col2:
        account_number = st.text_input("Account Number *", max_chars=10)

    st.markdown("---")
    st.markdown("### 🚨 Emergency Contact")
    col1, col2 = st.columns(2)
    with col1:
        emergency_name = st.text_input("Contact Name *")
        emergency_relationship = st.text_input("Relationship *")
    with col2:
        emergency_phone = st.text_input("Contact Phone *")

    st.markdown("---")
    submit = st.form_submit_button("⛏️ Create Account", type="primary", use_container_width=True)

if submit:
    # Validate passwords match
    if password != confirm_password:
        st.error("❌ Passwords do not match.")
        st.stop()
    
    # Validate all required fields
    required_fields = {
        "Email": email,
        "Password": password,
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
        st.stop()
    
    try:
        # Create auth user
        auth_res = supabase.auth.sign_up({"email": email, "password": password})
        if not auth_res.user:
            st.error("Signup failed. Please try again.")
            st.stop()
        
        user_id = auth_res.user.id
        
        # Insert into user_scans
        service.table("user_scans").insert({
            "user_id": user_id,
            "scans_remaining": 30,
            "plan": "free"
        }).execute()
        
        # Insert into user_profiles
        service.table("user_profiles").insert({
            "user_id": user_id,
            "first_name": first_name.strip(),
            "middle_name": middle_name.strip() if middle_name else None,
            "last_name": last_name.strip(),
            "gender": gender,
            "date_of_birth": date_of_birth.isoformat(),
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
            "mining_license_number": mining_license_number.strip() if mining_license_number else "N/A",
            "mining_cooperative": mining_cooperative.strip() if mining_cooperative else "N/A",
            "mining_type": mining_type,
            "account_name": account_name.strip(),
            "account_number": account_number.strip(),
            "bank_name": bank_name,
            "emergency_contact_name": emergency_name.strip(),
            "emergency_contact_phone": emergency_phone.strip(),
            "emergency_relationship": emergency_relationship.strip(),
            "verification_status": "pending",
        }).execute()
        
        st.success("✅ Account created successfully! 30 free scans added.")
        st.balloons()
        st.info("Please login with your new credentials.")
        st.page_link("app.py", label="Go to Login")
        
    except Exception as e:
        st.error(f"Error: {e}")
