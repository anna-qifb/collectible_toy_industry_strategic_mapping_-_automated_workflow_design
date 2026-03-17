import streamlit as st
import plotly.express as px
import requests
import json
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import datetime

st.set_page_config(page_title="Collectible Toy Strategy AI", layout="wide")
st.title("🎮 Collectible Toy Industry – Agentic Strategy Dashboard")
st.caption("Layer 1–3 insights • Data from uploaded JSON or default values • Live n8n trigger")

# ────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────
with st.sidebar:
    st.header("CEO Profile (HITL)")
    growth = st.selectbox("Financial emphasis", ["Growth", "Balanced", "Margin"], index=0)
    risk   = st.selectbox("Risk appetite",      ["Low", "Medium", "High"], index=1)
    region = st.selectbox("Primary region",     ["APAC", "NA", "EU", "GLOBAL"], index=0)
    channel = st.selectbox("Go-to-market",      ["DTC", "RETAIL", "LICENSING"], index=0)

    st.divider()
    st.header("Strategy Data Source")
    uploaded_json = st.file_uploader("Upload json file", type=["json"],
                                    help="Upload JSON containing mock data such as market data, forces, strategy statement")

    strategy_data = {}
    if uploaded_json is not None:
        try:
            strategy_data = json.load(uploaded_json)
            st.success(f"Loaded: {strategy_data.get('workflow_name', 'Custom Strategy Data')}")
        except Exception as e:
            st.error(f"Invalid JSON format: {e}")
            strategy_data = {}

    st.divider()
    st.header("n8n Live Trigger")
    webhook_url = st.text_input("Webhook URL", placeholder="https://your-n8n-instance/webhook/...")

    if st.button("🚀 Run Full Strategy Workflow", type="primary", use_container_width=True):
        if not webhook_url.strip():
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
                    st.success(f"Triggered successfully (HTTP {resp.status_code})")
                    st.session_state.last_run = f"Success • {resp.elapsed.total_seconds():.2f}s"
                    st.session_state.last_run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S JST")
                else:
                    st.error(f"Webhook failed • HTTP {resp.status_code}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

# Helper to get value from JSON or fallback
def get_data(path, default):
    current = strategy_data
    for key in path.split('.'):
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

# ────────────────────────────────────────────────
# TABS
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
        market_data = get_data("layer1", {})
        years = ["2024", "2025", "2026", "2027", "2028", "2029", "2030"]
        values = [float(market_data.get("market_2024", 24.9))] + \
                 [float(market_data.get("market_2030", 40.2)) * (1 + float(market_data.get("cagr", 8.3))/100)**(i-1) for i in range(1,7)]
        fig = px.line(x=years, y=values, markers=True,
                      title=f"Global Collectible Toys Market · {market_data.get('cagr', '8.3')}% CAGR")
        fig.update_layout(yaxis_title="Market Size (USD B)", height=380)
        st.plotly_chart(fig, use_container_width=True)

    colA, colB = st.columns(2)
    with colA:
        st.metric("2024 Market", f"${market_data.get('market_2024', '24.9')}B")
        st.metric("2030 Projection", f"${market_data.get('market_2030', '40.2')}B")
    with colB:
        st.metric("Kidult Share (est.)", f"{market_data.get('kidult_share', '30–40')}%")
        st.metric("APAC Driver", market_data.get('apec_driver', 'Blind boxes + DTC'))

# ───── Tab 2 ─────
with tab2:
    st.subheader("Layer 2 – Structural Analysis")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("**Porter’s Five Forces (score 1–10)**")
        forces = get_data("layer2.forces", {"Rivalry": 8, "New Entrants": 6, "Buyer Power": 7, "Supplier Power": 5, "Substitutes": 6})
        fig_forces = px.bar(x=list(forces.keys()), y=list(forces.values()),
                            color=list(forces.values()), color_continuous_scale="RdYlGn_r",
                            title="Force Intensity")
        st.plotly_chart(fig_forces, use_container_width=True)
    with col2:
        st.markdown("**Profit Pool Concentration**")
        pools = get_data("layer2.profit_pools", [
            {"segment": "DTC / Drops", "margin": "High"},
            {"segment": "Premium Statues", "margin": "High"},
            {"segment": "Blind Boxes", "margin": "Med-High"},
            {"segment": "Traditional Wholesale", "margin": "Low-Med"},
            {"segment": "IP Licensing (winners)", "margin": "High"}
        ])
        st.markdown("| Segment | Margin Level |\n|---------|--------------|")
        for p in pools:
            st.markdown(f"| {p['segment']} | {p['margin']} |")

# ───── Tab 3 ─────
with tab3:
    st.subheader("Layer 3 – Strategic Recommendation")
    st.success("**Collis & Rukstad-style Strategy Statement**")
    layer3 = get_data("layer3", {})
    st.markdown(f"**Objective**  \n{layer3.get('objective', 'Capture leading position in APAC kidult collectibles via DTC by 2027 (target ≥25% category share).')}")
    st.markdown(f"**Scope**  \n{layer3.get('scope', 'Blind boxes • premium designer figures • micro-IP<br>Primary geography: APAC (China + SEA)<br>Channel: DTC + owned community platforms')}")
    st.markdown(f"**Competitive Advantage**  \n{layer3.get('advantage', 'Fast viral IP incubation engine + strong brand/community flywheel<br>(aligned with design & fan-engagement strengths)')}")
    st.info(layer3.get('alignment_note', "Direction matches Growth focus • Medium risk • DTC preference"))

# ───── Tab 4 ─────
with tab4:
    st.subheader("Real Market Visuals 2024–2030")
    market_data = get_data("layer1", {})
    market = {"2024": float(market_data.get("market_2024", 24.9)),
              "2030": float(market_data.get("market_2030", 40.2))}
    fig_growth = px.line(x=list(market.keys()), y=list(market.values()), markers=True,
                         title="Collectible Toy Market Projection (USD Billion)")
    st.plotly_chart(fig_growth, use_container_width=True)

    comps = get_data("competitors_2024", {"Pop Mart":1.80, "Pokémon TCG":2.20, "Bandai Hobby":1.60, "Funko":1.05})
    fig_comp = px.bar(x=list(comps.keys()), y=list(comps.values()),
                      title="Estimated 2024 Leader Revenues (USD Billion)",
                      color=list(comps.values()), color_continuous_scale="Blues")
    st.plotly_chart(fig_comp, use_container_width=True)

# ───── Tab 5 ─────
with tab5:
    st.subheader("n8n Workflow Execution")
    if "last_run" in st.session_state:
        st.success("Last execution:")
        st.code(st.session_state.last_run, language=None)
    else:
        st.info("Click «Run Full Strategy Workflow» in the sidebar to start the chain.")

# ────────────────────────────────────────────────
# PDF
# ────────────────────────────────────────────────
def generate_summary_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []
    elements.append(Paragraph("Collectible Toy Strategy Summary", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Generated: {st.session_state.get('last_run_time', 'N/A')}", styles['Normal']))
    elements.append(Spacer(1, 24))

    # CEO Profile
    elements.append(Paragraph("CEO Profile (HITL)", styles['Heading2']))
    data = [["Financial emphasis", growth], ["Risk appetite", risk],
            ["Primary region", region], ["Go-to-market", channel]]
    t = Table(data, colWidths=[140, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND',(0,1),(-1,-1),colors.beige),
        ('GRID',(0,0),(-1,-1),1,colors.black)
    ]))
    elements.append(t)
    elements.append(Spacer(1, 24))

    # Pull from JSON or fallback
    l1 = get_data("layer1", {})
    elements.append(Paragraph("Layer 1 – Market Context", styles['Heading2']))
    elements.append(Paragraph(f"2024 Market: ${l1.get('market_2024', '24.9')}B", styles['Normal']))
    elements.append(Paragraph(f"2030 Projection: ${l1.get('market_2030', '40.2')}B (~{l1.get('cagr', '8.3')}% CAGR)", styles['Normal']))
    elements.append(Paragraph(f"Kidult share est. {l1.get('kidult_share', '30–40')}%", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Layer 2 – Forces & Profit Pools", styles['Heading2']))
    f = get_data("layer2.forces", {})
    forces_text = f"Rivalry {f.get('Rivalry',8)}/10, Buyers {f.get('Buyer Power',7)}/10, Entrants {f.get('New Entrants',6)}/10, Suppliers {f.get('Supplier Power',5)}/10, Substitutes {f.get('Substitutes',6)}/10"
    elements.append(Paragraph(forces_text, styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Layer 3 – Recommended Strategy", styles['Heading2']))
    l3 = get_data("layer3", {})
    strategy_text = f"Objective: {l3.get('objective', '…')}<br/>Scope: {l3.get('scope', '…')}<br/>Advantage: {l3.get('advantage', '…')}"
    elements.append(Paragraph(strategy_text, styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# PDF button
if "last_run" in st.session_state and "Success" in st.session_state.get("last_run", ""):
    st.success("Workflow completed successfully → PDF summary available")
    pdf_buffer = generate_summary_pdf()
    st.download_button(
        label="📄 Download Layer Summary PDF",
        data=pdf_buffer,
        file_name="collectible_toy_strategy_summary.pdf",
        mime="application/pdf"
    )

st.divider()
st.caption("Updated March 2026 • Data can be overridden by uploaded JSON • HK time")
