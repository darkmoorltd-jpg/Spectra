
import streamlit as st
import streamlit.components.v1 as components
import uuid
from utils.auth import get_current_user
from utils.paystack import PAYSTACK_PUBLIC_KEY

st.set_page_config(page_title="Buy Scans", page_icon="💳", layout="wide")

st.title("💳 Buy Scans")
st.markdown("Purchase additional scans or subscribe for unlimited access.")

user = get_current_user()
if user is None:
    st.warning("Please log in to buy scans.")
    st.stop()

PLANS = {
    "10": {"scans": 10, "price": "₦500", "kobo": 50000},
    "25": {"scans": 25, "price": "₦1,000", "kobo": 100000},
    "60": {"scans": 60, "price": "₦2,000", "kobo": 200000},
    "unlimited": {"scans": 9999, "price": "₦2,000/month", "kobo": 200000},
}

cols = st.columns(len(PLANS))
for i, (key, plan) in enumerate(PLANS.items()):
    with cols[i]:
        st.markdown(f"### {plan['scans']} Scans")
        st.markdown(f"**{plan['price']}**")
        if st.button("Select", key=f"plan_{key}"):
            st.session_state.selected_plan = key
            st.rerun()

if "selected_plan" in st.session_state:
    selected = st.session_state.selected_plan
    plan = PLANS[selected]
    ref = f"SPECTRA_{user.id[:8]}_{selected}_{uuid.uuid4().hex[:6]}"

    st.markdown("---")
    st.markdown(f"### Selected: {plan['scans']} scans for {plan['price']}")

    # Paystack inline payment
    email = user.email if user.email else "miner@spectra.ng"
    amount_kobo = plan["kobo"]

    components.html(f"""
    <button onclick="payWithPaystack()" style="background:#2e7d32;color:white;border:none;padding:15px 30px;border-radius:8px;font-size:1.2rem;cursor:pointer;">
        Pay {plan['price']} Now
    </button>
    <script src="https://js.paystack.co/v1/inline.js"></script>
    <script>
        function payWithPaystack() {{
            const handler = PaystackPop.setup({{
                key: '{PAYSTACK_PUBLIC_KEY}',
                email: '{email}',
                amount: {amount_kobo},
                currency: 'NGN',
                ref: '{ref}',
                label: 'SPECTRA Scans',
                callback: function(response) {{
                    window.location.href = '/payment_callback?reference=' + response.reference + '&plan={selected}';
                }},
                onClose: function() {{
                    alert('Payment cancelled.');
                }}
            }});
            handler.openIframe();
        }}
    </script>
    """, height=100)

    st.info("After payment, you will be redirected to confirm your scans.")
