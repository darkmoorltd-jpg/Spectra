
import streamlit as st
import requests

def get_market_insight(mineral: str, grade: float, value_ngn: float) -> str:
    """Return AI-generated market insight. Falls back to static text if no API key."""
    try:
        api_key = st.secrets["deepseek"]["api_key"]
        prompt = f"Give a brief market insight for {mineral} with grade {grade*100:.0f}% in Nigeria. Price per tonne ₦{value_ngn:,.0f}."
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are SPECTRA, a mineral market expert."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 300
        }
        r = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload, timeout=15)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"Market insight unavailable (API error {r.status_code})."
    except Exception as e:
        # Fallback static
        return f"Current average price for {mineral} in Nigeria is about ₦{value_ngn:,.0f} per tonne. Consider selling at major mining markets in Jos or Abuja."
