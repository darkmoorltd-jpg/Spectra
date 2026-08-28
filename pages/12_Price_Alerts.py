from utils.sidebar import render_sidebar

import streamlit as st
from utils.style import apply_global_style
from utils.auth import get_current_user
from utils.price_alerts import add_price_alert, get_user_alerts
from utils.constants import MINERALS
from utils.session import init_session

init_session()
st.set_page_config(page_title="Price Alerts", page_icon="🔔", layout="wide")
render_sidebar()
apply_global_style()

st.markdown('<h2 style="text-align:center;">🔔 Price Alerts</h2>', unsafe_allow_html=True)

user = get_current_user()
if user is None:
    st.warning("Please login to set price alerts.")
else:
    with st.form("alert_form"):
        mineral = st.selectbox("Mineral", MINERALS)
        target_price = st.number_input("Target Price (₦/kg)", min_value=0.0, value=1000.0)
        submit = st.form_submit_button("Set Alert")
        if submit:
            ok, err = add_price_alert(user.id, mineral, target_price)
            if ok:
                st.success("Alert set!")
            else:
                st.error(f"Error: {err}")

    st.markdown("### Your Active Alerts")
    alerts = get_user_alerts(user.id)
    if alerts:
        for a in alerts:
            st.markdown(f"- {a['mineral']} at ₦{a['target_price']}/kg")
    else:
        st.info("No active alerts.")