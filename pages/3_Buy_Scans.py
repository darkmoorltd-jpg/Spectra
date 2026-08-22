
import streamlit as st

st.set_page_config(page_title="Buy Scans", page_icon="💳", layout="wide")

st.title("💳 Buy Scans")
st.markdown("Purchase additional scans or subscribe for unlimited access.")

# Demo plans (replace with actual Paystack integration later)
plans = {
    "10 Scans": {"price": "₦500", "kobo": 50000},
    "25 Scans": {"price": "₦1,000", "kobo": 100000},
    "60 Scans": {"price": "₦2,000", "kobo": 200000},
    "Unlimited (Monthly)": {"price": "₦2,000/month", "kobo": 200000}
}

cols = st.columns(len(plans))
for i, (name, p) in enumerate(plans.items()):
    with cols[i]:
        st.markdown(f"### {name}")
        st.markdown(f"**{p['price']}**")
        if st.button(f"Select {name}", key=f"plan_{i}"):
            st.session_state.selected_plan = name
            st.rerun()

if "selected_plan" in st.session_state:
    selected = st.session_state.selected_plan
    st.success(f"Selected: {selected}")
    st.info("Payment gateway will be integrated here (Paystack).")
    # Placeholder Paystack button will go here
