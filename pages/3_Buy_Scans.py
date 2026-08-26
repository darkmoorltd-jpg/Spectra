from utils.sidebar import render_sidebar

import streamlit as st
import streamlit.components.v1 as components
import uuid
from utils.style import apply_global_style
from utils.auth import get_current_user
from utils.paystack import PAYSTACK_PUBLIC_KEY

st.set_page_config(page_title="Buy Scans", page_icon="💳", layout="wide")
render_sidebar()
apply_global_style()

st.markdown('<h2 style="text-align:center;">💳 Buy Scans</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#8892b0;">Choose a plan and power up your mining</p>', unsafe_allow_html=True)

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
        st.markdown(f"""
        <div class="scan-card" style="text-align:center;">
            <h3 style="color:#ffd700;">{plan['scans']} Scans</h3>
            <h2 style="color:#fff;">{plan['price']}</h2>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select", key=f"plan_{key}"):
            st.session_state.selected_plan = key
            st.rerun()

if "selected_plan" in st.session_state:
    selected = st.session_state.selected_plan
    plan = PLANS[selected]
    ref = f"SPECTRA_{user.id[:8]}_{selected}_{uuid.uuid4().hex[:6]}"

    st.markdown("---")
    st.markdown(f"### Selected: {plan['scans']} scans for {plan['price']}")

    email = user.email if user.email else "miner@spectra.ng"
    amount_kobo = plan["kobo"]

    components.html(f"""
    <button onclick="payWithPaystack()" style="background:linear-gradient(135deg,#1f2a44,#111827);color:#ffd700;border:1px solid #ffd700;border-radius:8px;padding:15px 30px;font-size:1.2rem;font-weight:600;cursor:pointer;box-shadow:0 0 15px rgba(255,215,0,0.3);">
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
    """, height=120)

    st.info("After payment, you will be redirected to confirm your scans.")