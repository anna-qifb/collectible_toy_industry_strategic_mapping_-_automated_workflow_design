import streamlit as st
import plotly.express as px
import requests
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import datetime

st.session_state.last_run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S JST")
st.set_page_config(page_title="Collectible Toy Strategy AI", layout="wide")
st.title("🎮 Collectible Toy Industry – Agentic Strategy Dashboard")
st.caption("Layer 1–3 insights • mock market data • live n8n trigger")

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
                    st.session_state.last_run = f"Success • {resp.elapsed.total_seconds():.2f}s • {resp.text[:140]}..."
                else:
                    st.error(f"Webhook failed • HTTP {resp.status_code}\n{resp.text[:220]}")
            except Exception as e:
                st.error(f"Connection error:\n{str(e)}")

# ────────────────────────────────────────────────
#  MAIN TABS
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
                      title="Global Collectible Toys Market (USD Billion) · ~8.3% CAGR")
        fig.update_layout(yaxis_title="Market Size (USD B)", height=380)
        st.plotly_chart(fig, use_container_width=True)

    colA, colB = st.columns(2)
    with colA:
        st.metric("2024 Market", "$24.9B")
        st.metric("2030 Projection", "$40.2B")
    with colB:
        st.metric("Kidult Share (est.)", "30–40%")
        st.metric("APAC Driver", "Blind boxes + DTC")

# ───── Tab 2 ─────
with tab2:
    st.subheader("Layer 2 – Structural Analysis")
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("**Porter’s Five Forces (score 1–10)**")
        forces = {"Rivalry": 8, "New Entrants": 6, "Buyer Power": 7, "Supplier Power": 5, "Substitutes": 6}
        fig_forces = px.bar(x=list(forces.keys()), y=list(forces.values()),
                            color=list(forces.values()), color_continuous_scale="RdYlGn_r",
                            title="Force Intensity")
        st.plotly_chart(fig_forces, use_container_width=True)

    with col2:
        st.markdown("**Profit Pool Concentration**")
        st.markdown("""
        | Segment              | Margin Level    |
        |----------------------|-----------------|
        | DTC / Drops          | High            |
        | Premium Statues      | High            |
        | Blind Boxes          | Med-High        |
        | Traditional Wholesale| Low-Med         |
        | IP Licensing (winners)| High           |
        """)

# ───── Tab 3 ─────
with tab3:
    st.subheader("Layer 3 – Strategic Recommendation")
    st.success("**Collis & Rukstad-style Strategy Statement**")
    st.markdown("""
    **Objective**  
    Capture leading position in APAC kidult collectibles via DTC by 2027 (target ≥25% category share).

    **Scope**  
    Blind boxes • premium designer figures • micro-IP  
    Primary geography: APAC (China + SEA)  
    Channel: DTC + owned community platforms

    **Competitive Advantage**  
    Fast viral IP incubation engine + strong brand/community flywheel  
    (aligned with design & fan-engagement strengths)
    """)

    st.info("Direction matches Growth focus • Medium risk • DTC preference")

# ───── Tab 4 ─────
with tab4:
    st.subheader("Real Market Visuals 2024–2030")

    market = {"2024":24.9,"2025":27.0,"2026":29.3,"2027":31.8,"2028":34.5,"2029":37.4,"2030":40.2}
    fig_growth = px.line(x=list(market.keys()), y=list(market.values()), markers=True,
                         title="Collectible Toy Market Projection (USD Billion)")
    st.plotly_chart(fig_growth, use_container_width=True)

    comps = {"Pop Mart":1.80, "Pokémon TCG":2.20, "Bandai Hobby":1.60, "Funko":1.05}
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

st.divider()
st.caption("Updated 2025–2026 • Data: industry reports, Pop Mart filings, Circana & similar estimates")

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
    data = [
        ["Financial emphasis", growth],
        ["Risk appetite", risk],
        ["Primary region", region],
        ["Go-to-market", channel],
    ]
    t = Table(data, colWidths=[120, 300])
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

    # Layer 1 highlights (text only – charts are hard in PDF without images)
    elements.append(Paragraph("Layer 1 – Market Context", styles['Heading2']))
    elements.append(Paragraph(f"2024 Market: $24.9B", styles['Normal']))
    elements.append(Paragraph(f"2030 Projection: $40.2B (~8.3% CAGR)", styles['Normal']))
    elements.append(Paragraph("Kidult share est. 30–40%", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Layer 2
    elements.append(Paragraph("Layer 2 – Forces & Profit Pools", styles['Heading2']))
    forces_text = "Porter’s Forces: Rivalry 8/10, Buyers 7/10, Entrants 6/10, Suppliers 5/10, Substitutes 6/10"
    elements.append(Paragraph(forces_text, styles['Normal']))
    elements.append(Spacer(1, 12))

    # Layer 3 – Strategy Statement
    elements.append(Paragraph("Layer 3 – Recommended Strategy", styles['Heading2']))
    strategy_text = """
    Objective: Capture leading position in APAC kidult collectibles via DTC by 2027 (≥25% share).<br/>
    Scope: Blind boxes, premium figures, micro-IP | APAC focus | DTC channels.<br/>
    Advantage: Fast viral IP incubation + brand/community flywheel.
    """
    elements.append(Paragraph(strategy_text, styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return buffer


if "last_run" in st.session_state and "Success" in st.session_state.last_run:
    st.success("Workflow completed successfully → PDF summary available")
    
    pdf_buffer = generate_summary_pdf()
    
    st.download_button(
        label="📄 Download Layer Summary PDF",
        data=pdf_buffer,
        file_name="collectible_toy_strategy_summary.pdf",
        mime="application/pdf",
        key="pdf_download"
    )
