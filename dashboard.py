import streamlit as st
import pandas as pd
import sqlite3

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
    type="password"
)

st.sidebar.divider()
st.sidebar.success("Compliance Mode: DPDP Act 2023 🇮🇳")

# --- DATABASE CONNECTION ---
conn = sqlite3.connect("audit_logs.db")

df = pd.read_sql_query("SELECT * FROM logs", conn)

# --- Metrics ---
total_prompts = len(df)
total_pii = len(df)
latency = round(df["latency"].mean(), 2) if not df.empty else 0
pr = round(total_pii / total_prompts, 2) if total_prompts > 0 else 0

# --- Metric Cards ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📨 Total Prompts", total_prompts)

with col2:
    st.metric("🔒 PII Protected", total_pii)

with col3:
    st.metric("⚡ Avg Latency (s)", latency)

with col4:
    st.metric("📊 Protection Ratio", pr)

# --- Chart: PII Distribution ---
st.subheader("📊 PII Detection Distribution")

if not df.empty:
    chart_data = df.groupby("entity_type").size()
    st.bar_chart(chart_data)
else:
    st.info("No data available for chart yet.")

# --- RMF (Risk Mitigation Factor) ---
st.subheader("🧠 Risk Mitigation Factor (RMF)")

# Risk weights
risk_weights = {
    "AADHAAR_NUMBER": 10,
    "PAN_NUMBER": 8,
    "INDIAN_PHONE_NUMBER": 5,
    "PERSON": 2
}

rmf = 0

if not df.empty:
    for entity in df["entity_type"]:
        rmf += risk_weights.get(entity, 1)

st.metric("🚨 Risk Mitigated Score", rmf)

st.divider()

# --- Recent Logs ---
st.subheader("📋 Real-time Protection Log")

recent_logs = pd.read_sql_query(
    "SELECT * FROM logs ORDER BY timestamp DESC LIMIT 10",
    conn
)

st.dataframe(recent_logs, use_container_width=True)

# --- Refresh Button ---
if st.button("🔄 Refresh Data"):
    st.rerun()

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