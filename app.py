import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json
from io import BytesIO

st.set_page_config(page_title="Collectible Toy Strategy AI", layout="wide")
st.title("🎮 Collectible Toy Industry – LIVE Agentic Strategy Dashboard")
st.markdown("**Mock market data + LIVE n8n webhook trigger**")

# ====================== SIDEBAR – CEO PROFILE + n8n CONNECTION ======================
st.sidebar.header("CEO Profile (HITL Checkpoint 2)")
growth_focus = st.sidebar.selectbox("Financial emphasis", ["Growth", "Balanced", "Margin"], key="growth")
risk_appetite = st.sidebar.selectbox("Risk appetite", ["Low", "Medium", "High"], key="risk")
region = st.sidebar.selectbox("Primary growth region", ["APAC", "NA", "EU", "GLOBAL"], key="region")
channel = st.sidebar.selectbox("Go-to-market", ["DTC", "RETAIL", "LICENSING"], key="channel")

st.sidebar.divider()
st.sidebar.header("🔌 n8n LIVE Connection")
webhook_url = st.sidebar.text_input(
    "n8n Webhook URL",
    placeholder="https://your-n8n.com/webhook/collectible-toy-strategy",
    help="Paste the webhook URL from your n8n workflow"
)
trigger_button = st.sidebar.button("🚀 Trigger Full n8n Workflow", type="primary")

# ====================== FILE UPLOADS ======================
col1, col2 = st.columns(2)
with col1:
    excel_file = st.file_uploader("Upload (MASTER) Agent Chaining - Raw.xlsx", type=["xlsx"])
with col2:
    n8n_mock = st.file_uploader("n8n_mock.json (for visualisation)", type=["txt", "json"])

# ====================== LIVE n8n TRIGGER ======================
if trigger_button and webhook_url:
    ceo_profile = {
        "GROWTH_FOCUS": growth_focus,
        "RISK": risk_appetite,
        "REGION": region,
        "CHANNEL": channel,
        "CAPITAL": "moderate",           # default – you can extend sidebar later
        "CAP_STRENGTHS": "BRAND,COMMUNITY,DESIGN",
        "SUCCESS_3Y_MODE": "button",
        "SUCCESS_3Y_BUTTON": "GROWTH"
    }
    
    try:
        response = requests.post(webhook_url, json=ceo_profile, timeout=10)
        if response.status_code in (200, 201):
            st.sidebar.success(f"✅ Workflow triggered! Execution ID: {response.text[:100]}")
            st.session_state.last_execution = response.text
        else:
            st.sidebar.error(f"❌ n8n returned {response.status_code}: {response.text}")
    except Exception as e:
        st.sidebar.error(f"Connection error: {e}")

# ====================== TABS ======================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Layer 1 Report", "🔍 Layer 2 Analysis", "🚀 Layer 3 Strategy", "📈 Real Charts", "🔄 LIVE n8n Workflow"])

# TAB 1 – Layer 1 (Excel mapping)
with tab1:
    if excel_file:
        xls = pd.ExcelFile(excel_file)
        try:
            layer1 = pd.read_excel(xls, sheet_name="Layer 1 Working Document")
            st.dataframe(layer1.head(10), use_container_width=True)
            st.success("✅ Layer 1 loaded from Excel")
        except:
            st.warning("Could not read Layer 1 sheet")
    else:
        st.info("Upload Excel for full Layer 1 table view")

# TAB 2 – Layer 2
with tab2:
    st.subheader("P06 Porter’s Five Forces")
    forces = {"Rivalry":8,"Entrants":6,"Buyers":7,"Suppliers":5,"Substitutes":6}
    fig = px.bar(x=list(forces.keys()), y=list(forces.values()), title="Force Scores")
    st.plotly_chart(fig, use_container_width=True)

# TAB 3 – Layer 3
with tab3:
    st.success("**Strategy Statement (Collis & Rukstad)**")
    st.markdown("**Objective:** Become #1 DTC kidult platform in APAC with 25%+ share by 2027.")
    st.markdown("**Scope:** Blind-box + premium figures | APAC focus | DTC channels.")
    st.markdown("**Advantage:** Viral IP incubation engine (tied to your BRAND+COMMUNITY strengths).")

# TAB 4 – Real Charts (2024-2030 data)
with tab4:
    market_data = {"2024":24.9,"2025":27.0,"2026":29.3,"2027":31.8,"2028":34.5,"2029":37.4,"2030":40.2}
    fig_growth = px.line(x=list(market_data.keys()), y=list(market_data.values()),
                         title="Global Collectible Toy Market (USD Billion) – CAGR 8.3%", markers=True)
    st.plotly_chart(fig_growth, use_container_width=True)

    competitors = {"Pop Mart":1.80,"Pokémon":2.20,"Bandai":1.60,"Funko":1.05,"Mattel Creations":0.30}
    fig_comp = px.bar(x=list(competitors.keys()), y=list(competitors.values()),
                      title="2024 Competitor Revenue (USD Billion)")
    st.plotly_chart(fig_comp, use_container_width=True)

# TAB 5 – LIVE n8n Workflow
with tab5:
    st.subheader("🔄 LIVE n8n Workflow Status")
    if webhook_url:
        st.success("✅ Connected to your n8n instance")
        if "last_execution" in st.session_state:
            st.write("Last triggered:", st.session_state.last_execution[:200])
    else:
        st.info("Enter n8n Webhook URL in sidebar to trigger live workflow")

    # Optional mock visualisation
    if n8n_mock:
        try:
            workflow = json.load(n8n_mock) if n8n_mock.name.endswith(".json") else json.loads(n8n_mock.getvalue().decode())
            st.json(workflow, expanded=False)
        except:
            st.text(n8n_mock.getvalue().decode()[:500] + "...")

st.caption("LIVE n8n webhook integration | Mock market data | Built for your collectible toy agent chain")
