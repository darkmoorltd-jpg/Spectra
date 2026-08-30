# VERSION 2.0 - Full Signup

import streamlit as st
from supabase import create_client
import datetime

def render_sidebar():
    with st.sidebar:
        st.markdown("## ⛏️ SPECTRA Account")
        user = st.session_state.get("user", None)
        
        if user is None:
            auth_choice = st.radio("Login / Signup", ["Login", "Signup"], key="sidebar_auth_choice")
            
            if auth_choice == "Login":
                email = st.text_input("Email", key="sidebar_login_email")
                password = st.text_input("Password", type="password", key="sidebar_login_password")
                if st.button("Login", key="sidebar_login_btn", use_container_width=True):
                    if email and password:
                        try:
                            url = st.secrets["supabase"]["url"]
                            key = st.secrets["supabase"]["key"]
                            client = create_client(url, key)
                            res = client.auth.sign_in_with_password({"email": email, "password": password})
                            if res.user:
                                st.session_state.user = res.user
                                st.success("Logged in!")
                                st.rerun()
                            else:
                                st.error("Login failed")
                        except Exception as e:
                            st.error(f"Error: {e}")
                    else:
                        st.warning("Email and password required.")
            
            else:  # Signup - Direct fields, no expander
                st.markdown("### 📋 Create Account")
                st.markdown("All fields required except Middle Name")
                
                # Account credentials
                email = st.text_input("Email *", key="su_email")
                password = st.text_input("Password *", type="password", key="su_password")
                confirm_password = st.text_input("Confirm Password *", type="password", key="su_confirm")
                
                st.markdown("---")
                
                # Personal info
                first_name = st.text_input("First Name *", key="su_first")
                middle_name = st.text_input("Middle Name (Optional)", key="su_middle")
                last_name = st.text_input("Last Name *", key="su_last")
                gender = st.selectbox("Gender *", ["", "Male", "Female"], key="su_gender")
                date_of_birth = st.date_input("Date of Birth *", key="su_dob", min_value=datetime.date(1940,1,1), max_value=datetime.date.today())
                marital_status = st.selectbox("Marital Status *", ["", "Single", "Married", "Divorced", "Widowed"], key="su_marital")
                phone = st.text_input("Phone *", key="su_phone")
                whatsapp = st.text_input("WhatsApp *", key="su_whatsapp")
                
                st.markdown("---")
                
                # Address
                COUNTRIES = ["Nigeria", "Niger", "Ghana", "Mali", "Burkina Faso", "Tanzania", "DRC", "Zimbabwe", "South Africa", "Other"]
                country = st.selectbox("Country *", COUNTRIES, key="su_country")
                state = st.text_input("State *", key="su_state")
                lga = st.text_input("LGA *", key="su_lga")
                city = st.text_input("City/Town *", key="su_city")
                street = st.text_input("Street Address *", key="su_street")
                landmark = st.text_input("Landmark *", key="su_landmark")
                postal = st.text_input("Postal Code *", key="su_postal")
                
                st.markdown("---")
                
                # KYC
                bvn = st.text_input("BVN (11 digits) *", key="su_bvn", max_chars=11)
                nin = st.text_input("NIN (11 digits) *", key="su_nin", max_chars=11)
                id_type = st.selectbox("ID Type *", ["", "National ID Card", "Driver's License", "International Passport", "Voter's Card", "NIN Slip"], key="su_idtype")
                id_number = st.text_input("ID Number *", key="su_idnum")
                
                st.markdown("---")
                
                # Mining
                mining_state = st.text_input("Mining State *", key="su_mstate")
                mining_lga = st.text_input("Mining LGA *", key="su_mlga")
                mining_address = st.text_input("Mining Address *", key="su_maddr")
                minerals = st.text_input("Minerals of Interest *", key="su_minerals")
                years_exp = st.number_input("Years of Mining Experience *", min_value=0, value=0, key="su_years")
                license_num = st.text_input("Mining License Number *", key="su_license", placeholder="N/A if none")
                cooperative = st.text_input("Mining Cooperative *", key="su_coop", placeholder="N/A if none")
                mining_type = st.selectbox("Mining Type *", ["", "Artisanal", "Small-scale", "Medium-scale", "Large-scale"], key="su_mtype")
                
                st.markdown("---")
                
                # Bank
                account_name = st.text_input("Account Name *", key="su_acctname")
                bank_name = st.selectbox("Bank *", ["", "Access Bank", "GTBank", "Zenith Bank", "UBA", "First Bank", "Kuda", "Opay", "Palmpay", "Moniepoint", "Sterling Bank", "Union Bank", "Fidelity Bank", "Wema Bank"], key="su_bank")
                account_number = st.text_input("Account Number *", key="su_acctnum", max_chars=10)
                
                st.markdown("---")
                
                # Emergency
                em_name = st.text_input("Emergency Contact Name *", key="su_emname")
                em_relation = st.text_input("Relationship *", key="su_emrel")
                em_phone = st.text_input("Emergency Contact Phone *", key="su_emphone")
                
                st.markdown("---")
                
                if st.button("⛏️ Create Account", key="sidebar_signup_btn", use_container_width=True):
                    # Validate
                    if len(password) < 6:
                        st.error("❌ Password must be at least 6 characters.")
                    elif password != confirm_password:
                        st.error("❌ Passwords do not match.")
                    elif not all([email, password, first_name, last_name, gender, date_of_birth, marital_status, phone, whatsapp, country, state, lga, city, street, landmark, postal, bvn, nin, id_type, id_number, mining_state, mining_lga, mining_address, minerals, license_num, cooperative, mining_type, account_name, account_number, bank_name, em_name, em_relation, em_phone]):
                        st.error("❌ All fields are required except Middle Name.")
                    else:
                        try:
                            url = st.secrets["supabase"]["url"]
                            key = st.secrets["supabase"]["key"]
                            service_key = st.secrets["supabase"]["service_key"]
                            client = create_client(url, key)
                            service = create_client(url, service_key)
                            
                            # Create auth user
                            auth_res = client.auth.sign_up({"email": email, "password": password})
                            if not auth_res.user:
                                st.error("Signup failed.")
                            else:
                                user_id = auth_res.user.id
                                
                                # Insert scans
                                service.table("user_scans").insert({"user_id": user_id, "scans_remaining": 30, "plan": "free"}).execute()
                                
                                # Insert profile
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
                                    "street_address": street.strip(),
                                    "landmark": landmark.strip(),
                                    "postal_code": postal.strip(),
                                    "bvn": bvn.strip(),
                                    "nin": nin.strip(),
                                    "govt_id_type": id_type,
                                    "govt_id_number": id_number.strip(),
                                    "mining_state": mining_state.strip(),
                                    "mining_lga": mining_lga.strip(),
                                    "mining_address": mining_address.strip(),
                                    "minerals_of_interest": minerals.strip(),
                                    "years_mining_experience": years_exp,
                                    "mining_license_number": license_num.strip() if license_num else "N/A",
                                    "mining_cooperative": cooperative.strip() if cooperative else "N/A",
                                    "mining_type": mining_type,
                                    "account_name": account_name.strip(),
                                    "account_number": account_number.strip(),
                                    "bank_name": bank_name,
                                    "emergency_contact_name": em_name.strip(),
                                    "emergency_contact_phone": em_phone.strip(),
                                    "emergency_relationship": em_relation.strip(),
                                    "verification_status": "pending",
                                }).execute()
                                
                                st.session_state.user = auth_res.user
                                st.success("✅ Account created! 30 free scans added.")
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
        
        else:
            st.write(f"Logged in as: **{user.email}**")
            if st.button("Logout", key="sidebar_logout_btn", use_container_width=True):
                try:
                    url = st.secrets["supabase"]["url"]
                    key = st.secrets["supabase"]["key"]
                    client = create_client(url, key)
                    client.auth.sign_out()
                except:
                    pass
                st.session_state.user = None
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 🚀 Quick Navigation")
        pages = [
            ("🏠 Home", "/"),
            ("🔍 Scan Mineral", "/Scan_Mineral"),
            ("📊 My Vault", "/My_History"),
            ("💹 Market Prices", "/Market"),
            ("💳 Buy Scans", "/Buy_Scans"),
            ("👤 Profile", "/Profile"),
            ("📚 Mineralpedia", "/Mineralpedia"),
        ]
        for label, path in pages:
            st.markdown(f"[{label}]({path})")
