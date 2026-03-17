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
st.caption("Layer 1–3 insights • Real market data • Live n8n trigger + Workflow JSON Inspector")

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
    st.header("n8n Workflow JSON")
    uploaded_json = st.file_uploader("Upload n8n workflow JSON", type=["json"],
                                     help="Upload Latest N8N.json, n8n_mock.json or full n8n.json")

    if uploaded_json:
        try:
            workflow_data = json.load(uploaded_json)
            st.session_state.workflow_data = workflow_data
            st.success(f"✅ Loaded: {workflow_data.get('name', 'Unnamed Workflow')}")
        except Exception as e:
            st.error(f"Invalid JSON: {e}")

    st.divider()
    st.header("n8n Live Trigger")
    webhook_url = st.text_input("Webhook URL", placeholder="https://your-n8n-instance/webhook/...")

    if st.button("🚀 Run Full Strategy Workflow", type="primary", use_container_width=True):
        if not webhook_url.strip():
            st.error("Please enter webhook URL")
        else:
            payload = {
                "GROWTH_FOCUS": growth, "RISK": risk, "REGION": region, "CHANNEL": channel,
                "CAPITAL": "moderate", "CAP_STRENGTHS": "BRAND,COMMUNITY,DESIGN",
                "SUCCESS_3Y_MODE": "button", "SUCCESS_3Y_BUTTON": "GROWTH"
            }
            try:
                resp = requests.post(webhook_url, json=payload, timeout=12)
                if resp.status_code in (200, 202):
                    st.success(f"Triggered! (HTTP {resp.status_code})")
                    st.session_state.last_run = f"Success • {resp.elapsed.total_seconds():.2f}s"
                    st.session_state.last_run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S JST")
                else:
                    st.error(f"Failed {resp.status_code}")
            except Exception as e:
                st.error(f"Error: {e}")

# ────────────────────────────────────────────────
# TABS (your existing tabs 1–5 code goes here — omitted for brevity)
# tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([...])
# ... paste your tab content for Layer 1 to Workflow Inspector ...
# ────────────────────────────────────────────────

# ────────────────────────────────────────────────
# PDF GENERATION FUNCTION
# ────────────────────────────────────────────────
def generate_summary_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Collectible Toy Strategy Summary", styles['Title']))
    elements.append(Spacer(1, 12))

    # Add generation time
    elements.append(Paragraph(f"Generated: {st.session_state.get('last_run_time', 'N/A')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Workflow info (safe access — only if uploaded)
    wf_name = "None"
    node_count = 0
    if "workflow_data" in st.session_state:
        wf = st.session_state.workflow_data
        wf_name = wf.get('name', 'Unnamed')
        node_count = len(wf.get('nodes', []))

    elements.append(Paragraph(f"Workflow Used: {wf_name} ({node_count} nodes)", styles['Normal']))
    elements.append(Spacer(1, 24))

    # CEO Profile
    elements.append(Paragraph("CEO Profile (HITL)", styles['Heading2']))
    data = [
        ["Financial emphasis", growth],
        ["Risk appetite", risk],
        ["Primary region", region],
        ["Go-to-market", channel],
    ]
    t = Table(data, colWidths=[140, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(t)
    elements.append(Spacer(1, 24))

    # Layer 1
    elements.append(Paragraph("Layer 1 – Market Context", styles['Heading2']))
    elements.append(Paragraph("2024 Market: $24.9B", styles['Normal']))
    elements.append(Paragraph("2030 Projection: $40.2B (~8.3% CAGR)", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Layer 2
    elements.append(Paragraph("Layer 2 – Forces & Profit Pools", styles['Heading2']))
    elements.append(Paragraph("Porter’s Forces: Rivalry 8/10, Buyers 7/10, Entrants 6/10, Suppliers 5/10, Substitutes 6/10", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Layer 3
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

# ────────────────────────────────────────────────
# PDF DOWNLOAD BUTTON (now correctly placed at root level)
# ────────────────────────────────────────────────
if "last_run" in st.session_state and "Success" in st.session_state.get("last_run", ""):
    st.success("Workflow completed → PDF ready")
    pdf_buffer = generate_summary_pdf()
    st.download_button(
        label="📄 Download Full Strategy PDF",
        data=pdf_buffer,
        file_name="collectible_toy_strategy_summary.pdf",
        mime="application/pdf"
    )

st.divider()
st.caption("Enhanced with n8n JSON Inspector • Ready for GitHub + n8n testing • Fixed indentation March 2026")
