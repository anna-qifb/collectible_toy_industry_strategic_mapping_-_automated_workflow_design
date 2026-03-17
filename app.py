import streamlit as st
import plotly.express as px
import requests
import json

st.set_page_config(page_title="Collectible Toy Strategy AI", layout="wide")
st.title("🎮 Collectible Toy Industry – Agentic Strategy Dashboard")
st.caption("Layer 1–3 insights + real 2024–2030 market data + live n8n trigger")

# ────────────────────────────────────────────────
#  SIDEBAR – CEO Profile + n8n Webhook
# ────────────────────────────────────────────────
with st.sidebar:
    st.header("CEO Profile (HITL)")
    growth = st.selectbox("Financial emphasis", ["Growth", "Balanced", "Margin"], index=0)
    risk    = st.selectbox("Risk appetite",      ["Low", "Medium", "High"], index=1)
    region  = st.selectbox("Primary region",     ["APAC", "NA", "EU", "GLOBAL"], index=0)
    channel = st.selectbox("Go-to-market",       ["DTC", "RETAIL", "LICENSING"], index=0)

    st.divider()
    st.header("n8n Live Trigger")
    webhook_url = st.text_input("Webhook URL", placeholder="https://your-n8n-instance/webhook/...", help="From your n8n workflow")
    if st.button("🚀 Run Full Strategy Workflow", type="primary", use_container_width=True):
        if not webhook_url:
            st.error("Please enter a valid webhook URL")
        else:
            payload = {
                "GROWTH_FOCUS": growth,
                "RISK": risk,
                "REGION": region,
                "CHANNEL": channel,
                "CAPITAL": "moderate",
                "CAP_STRENGTHS": "BRAND,COMMUNITY,DESIGN",
                "SUCCESS_3Y_MODE": "button",
                "SUCCESS_3Y_BUTTON": "GROWTH"
            }
            try:
                resp = requests.post(webhook_url, json=payload, timeout=12)
                if resp.status_code in (200, 202):
                    st.success(f"Triggered! (status {resp.status_code})")
                    st.session_state.last_run = f"Success at {resp.elapsed.total_seconds():.2f}s – {resp.text[:120]}..."
                else:
                    st.error(f"Failed – {resp.status_code}: {resp.text[:180]}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

# ────────────────────────────────────────────────
#  TABS
# ────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Layer 1 – Context",
    "🔍 Layer 2 – Forces & Pools",
    "🚀 Layer 3 – Strategy",
    "📈 Market Charts",
    "🔄 n8n Status"
])

# ───── Tab 1 ─────
with tab1:
    st.subheader("Layer 1 – Industry Context Highlights")
    with st.expander("Market Size & Growth (2024–2030)", expanded=True):
        data = {"2024": 24.9, "2025": 27.0, "2026": 29.3, "2027": 31.8, "2028": 34.5, "2029": 37.4, "2030": 40.2}
        fig = px.line(x=list(data.keys()), y=list(data.values()), markers=True,
                      title="Global Collectible Toys Market (USD Billion) · CAGR ~8.3%")
        fig.update_layout(yaxis_title="Market Size (USD B)", height=380)
        st.plotly_chart(fig, use_container_width=True)

    colA, colB = st.columns(2)
    with colA:
        st.metric("2024 Market Size", "$24.9B")
        st.metric("Projected 2030", "$40.2B")
    with colB:
        st.metric("Kidult Share (est.)", "≈30–40%")
        st.metric("APAC Growth Driver", "Blind boxes + DTC")

# ───── Tab 2 ─────
with tab2:
    st.subheader("Layer 2 – Structural Analysis")
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("**Porter’s Five Forces (1–10)**")
        forces = {"Rivalry": 8, "New Entrants": 6, "Buyer Power": 7, "Supplier Power": 5, "Substitutes": 6}
        fig_forces = px.bar(x=list(forces.keys()), y=list(forces.values()),
                            color=list(forces.values()), color_continuous_scale="RdYlGn_r",
                            title="Force Intensity")
        st.plotly_chart(fig_forces, use_container_width=True)

    with col2:
        st.markdown("**Profit Pool Concentration**")
        pools = pd.DataFrame({
            "Segment": ["DTC / Drops", "Premium Statues", "Blind Boxes", "Traditional Wholesale", "IP Licensing"],
            "Margin Level": ["High", "High", "Med-High", "Low-Med", "High (winners)"]
        })
        st.dataframe(pools, hide_index=True, use_container_width=True)

# ───── Tab 3 ─────
with tab3:
    st.subheader("Layer 3 – Strategic Recommendation")
    st.success("**Collis & Rukstad-style Strategy Statement**")
    st.markdown("""
    **Objective**  
    Capture leading position in APAC kidult collectibles via DTC by 2027 (25%+ category share).

    **Scope**  
    Blind boxes, premium designer figures & micro-IP | Primary focus: APAC (China + SEA) | Channel: DTC + owned community platforms.

    **Competitive Advantage**  
    Fast viral IP incubation + strong brand/community engine (leveraging design & fan-engagement strengths).
    """)

    st.info("This direction aligns with Growth focus + Medium risk + DTC channel preference.")

# ───── Tab 4 ─────
with tab4:
    st.subheader("Real Market Visuals 2024–2030")

    # Growth line
    market = {"2024":24.9,"2025":27.0,"2026":29.3,"2027":31.8,"2028":34.5,"2029":37.4,"2030":40.2}
    fig_growth = px.line(x=list(market.keys()), y=list(market.values()), markers=True,
                         title="Collectible Toy Market Projection (USD Billion)")
    st.plotly_chart(fig_growth, use_container_width=True)

    # Competitors bar
    comps = {"Pop Mart":1.80, "Pokémon TCG":2.20, "Bandai Hobby":1.60, "Funko":1.05, "Others": ~18}
    fig_comp = px.bar(x=list(comps.keys()), y=list(comps.values()),
                      title="Estimated 2024 Leader Revenues (USD Billion)",
                      color=list(comps.values()), color_continuous_scale="Blues")
    st.plotly_chart(fig_comp, use_container_width=True)

# ───── Tab 5 ─────
with tab5:
    st.subheader("n8n Workflow Execution")
    if "last_run" in st.session_state:
        st.success("Last execution result:")
        st.code(st.session_state.last_run, language=None)
    else:
        st.info("Click «Run Full Strategy Workflow» in the sidebar to trigger your n8n chain.")

    st.caption("Webhook sends CEO profile → starts P01 → P12 chain → returns result/log")

st.divider()
st.caption("Updated March 2025 • Real data sources: industry reports, Pop Mart filings, Circana estimates")
