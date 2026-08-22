
import requests
import streamlit as st

PAYSTACK_SECRET_KEY = st.secrets["paystack"]["secret_key"]
PAYSTACK_PUBLIC_KEY = st.secrets.get("paystack", {}).get("public_key", "pk_live_3af5d245e74f86f0517d214b6872f4ac8236e057")

def verify_payment(reference):
    """Verify a Paystack transaction and return (success_bool, amount_paid, error_msg)."""
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            data = r.json()
            if data.get("data", {}).get("status") == "success":
                amount = data["data"]["amount"] / 100  # Convert kobo to Naira
                return True, amount, None
            else:
                return False, 0, data.get("data", {}).get("gateway_response", "Payment not successful")
        else:
            return False, 0, f"API error {r.status_code}"
    except Exception as e:
        return False, 0, str(e)
