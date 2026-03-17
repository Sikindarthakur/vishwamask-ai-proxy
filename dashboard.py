import streamlit as st
import pandas as pd
import random

# --- Page Config ---
st.set_page_config(page_title="VishwaMask Audit", layout="wide")

st.title("🛡️ Vishwa-Mask: DPDP Compliance Audit")
st.markdown("### Real-time Privacy Protection Monitoring")

# --- Sidebar ---
st.sidebar.header("⚙ Configuration")

provider = st.sidebar.selectbox(
    "LLM Provider",
    ["ollama", "gemini", "openai"]
)

api_key = st.sidebar.text_input(
    "API Key (Optional)",
    type="password",
    help="Used for cloud providers only"
)

st.sidebar.divider()
st.sidebar.success("Compliance Mode: DPDP Act 2023 🇮🇳")

# --- MOCK DATA (Day 9 only) ---
total_prompts = random.randint(80, 200)
total_pii = random.randint(150, 400)
latency = round(random.uniform(1.5, 6.0), 2)

# --- Metric Cards ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📨 Total Prompts", total_prompts)

with col2:
    st.metric("🔒 PII Protected", total_pii)

with col3:
    st.metric("⚡ Avg Latency (s)", latency)

with col4:
    pr = round(total_pii / total_prompts, 2)
    st.metric("📊 Protection Ratio", pr)

st.divider()

# --- Protection Log Table ---
st.subheader("📋 Real-time Protection Log")

log_data = pd.DataFrame([
    {
        "Timestamp": "10:45 AM",
        "Prompt": "Send money to Rahul",
        "Masked": "[PERSON_1]",
        "Provider": "ollama",
        "Status": "Protected"
    },
    {
        "Timestamp": "10:47 AM",
        "Prompt": "My Aadhaar is 1234-5678-9012",
        "Masked": "[AADHAAR_NUMBER_1]",
        "Provider": "gemini",
        "Status": "Protected"
    },
    {
        "Timestamp": "10:49 AM",
        "Prompt": "Call me at 9876543210",
        "Masked": "[INDIAN_PHONE_NUMBER_1]",
        "Provider": "ollama",
        "Status": "Protected"
    }
])

st.dataframe(log_data, use_container_width=True)

# --- Info Section ---
with st.expander("ℹ Why this matters (DPDP Act 2023)"):
    st.write("""
    Under India's Digital Personal Data Protection (DPDP) Act 2023, organizations must ensure that sensitive personal data is not exposed to unauthorized systems.

    **Vishwa-Mask ensures:**
    - ✔ PII is masked before leaving the local environment  
    - ✔ AI models never see real sensitive data  
    - ✔ Full audit trail for compliance  
    - ✔ Privacy-by-design architecture    

    This helps startups and developers stay compliant with Indian data laws.
    """)

# --- Footer ---
st.success("✅ VishwaMask is actively protecting user data!")