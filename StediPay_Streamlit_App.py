"""
StediPay — Streamlit Demo Application

LEGAL NOTICE: Pilot portfolio project by Hasret Ozan Sevim. All data is hypothetical.
No affiliation, partnership, or endorsement with any company, protocol, or brand mentioned.
All brand names are property of their respective owners.
Not financial or legal advice. Smart contracts unaudited, not for production.
Author accepts no legal or financial liability of any kind.
© 2024–2026 Hasret Ozan Sevim. All rights reserved.

Licensed under the Business Source License 1.1 (BUSL-1.1).
Non-commercial / research use: permitted.
Commercial production use: requires a licence from Hasret Ozan Sevim.
See LICENSE file or contact hasretozan.sevim@unicam.it.

Blockchain timestamp: SHA-256 hash anchored on-chain as proof of creation date.

Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import time
import hashlib


DISCLAIMER_HTML = """
<div style='background:#1a0a00;border:1px solid #E67E22;border-left:5px solid #E67E22;
            padding:16px 20px;margin-bottom:20px;'>
  <div style='color:#E67E22;font-weight:700;font-size:0.9rem;margin-bottom:6px'>
    ⚠ Legal Disclaimer — Read Before Using This Demo
  </div>
  <div style='color:#aaa;font-size:0.78rem;line-height:1.7'>
    <strong style='color:#ccc'>Pilot portfolio project only.</strong>
    All data, projections, and metrics are strictly hypothetical and for illustrative purposes only.
    StediPay has <strong style='color:#ccc'>no affiliation, partnership, endorsement, or communication</strong>
    of any kind with any company, protocol, brand, or mentioned entity.
    All brand names are the property of their respective owners, referenced solely for illustrative purposes.
    Nothing here constitutes financial or legal advice. Smart contracts are unaudited and not for production use.
  <div style='color:#E67E22;font-weight:700;font-size:0.9rem;margin-bottom:6px'>
    ⚠ Technical Disclaimer
  <div style='color:#aaa;font-size:0.78rem;line-height:1.7'>
        <strong style='color:#ccc'>The demo is not currently integrated with a blockchain testnet.</strong>
        The demo of a live blockchain testnet will be integrated with Polygon Amoy and Ethereum Sepolia.
  </div>
</div>
"""

st.set_page_config(
    page_title="StediPay — Smart Stablecoin Payments",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(DISCLAIMER_HTML, unsafe_allow_html=True)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700&family=Barlow:wght@300;400;500&family=IBM+Plex+Mono:wght@300;400;500&display=swap');

  html, body, [class*="css"] { font-family: 'Barlow', sans-serif; }
  
  /* MAIN BACKGROUND – DARK BLUE */
  .stApp {
    background: #0A1F4E;
    color: #E0E9F5;
  }

  /* Sidebar – keep consistent dark */
  [data-testid="stSidebar"] {
    background: #06122E !important;
  }
  [data-testid="stSidebar"] * {
    color: #B8CCE8 !important;
  }
  [data-testid="stSidebar"] a {
    color: #7A9AD6 !important;
  }

  /* Metric cards */
  .metric-card {
    background: #0D264A;
    border: 1px solid #2A4878;
    border-left: 4px solid #C9A84C;
    border-radius: 0;
    padding: 16px 20px;
    margin: 6px 0;
  }
  .metric-val {
    font-size: 2rem;
    font-weight: 700;
    color: #F5F0E8;
    font-family: 'Barlow Condensed', sans-serif;
  }
  .metric-lbl {
    font-size: 0.75rem;
    color: #B8CCE8;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-family: 'IBM Plex Mono', monospace;
  }

  /* Step cards */
  .step-card {
    background: #0D264A;
    padding: 14px 18px;
    margin: 6px 0;
    border-left: 3px solid #C9A84C;
    border: 1px solid #2A4878;
  }
  .step-num {
    color: #C9A84C;
    font-weight: 600;
    font-family: 'IBM Plex Mono', monospace;
  }

  .tx-hash {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: #7A9AD6;
    background: #112B52;
    padding: 4px 8px;
  }

  /* Badges */
  .badge-green  { background:#103A2A; color:#5CD99A; padding:2px 10px; border:1px solid #1E7A4A; font-size:0.75rem; font-family:'IBM Plex Mono',monospace; }
  .badge-gold   { background:#2A2A10; color:#E8C87A; padding:2px 10px; border:1px solid #A8883A; font-size:0.75rem; font-family:'IBM Plex Mono',monospace; }
  .badge-teal   { background:#0D3A4A; color:#5BC8E0; padding:2px 10px; border:1px solid #2A7890; font-size:0.75rem; font-family:'IBM Plex Mono',monospace; }
  .badge-orange { background:#3A2A10; color:#F0A050; padding:2px 10px; border:1px solid #B87020; font-size:0.75rem; font-family:'IBM Plex Mono',monospace; }
  .badge-red    { background:#3A1010; color:#E08080; padding:2px 10px; border:1px solid #B04040; font-size:0.75rem; font-family:'IBM Plex Mono',monospace; }

  /* Headings */
  h1, h2, h3 {
    color: #F5F0E8 !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }

  /* Form labels */
  .stSelectbox label, .stNumberInput label, .stSlider label {
    color: #B8CCE8 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  /* Metric containers (Streamlit native) */
  div[data-testid="metric-container"] {
    background: #0D264A;
    border: 1px solid #2A4878;
    border-radius: 0;
    padding: 12px;
  }
  div[data-testid="metric-container"] label {
    color: #B8CCE8 !important;
  }
  div[data-testid="metric-container"] [data-testid="metric-value"] {
    color: #F5F0E8 !important;
  }

  /* Buttons */
  .stButton > button {
    background: #C9A84C;
    color: #0A1F4E;
    border: none;
    border-radius: 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
  }
  .stButton > button:hover {
    background: #D8B85C;
    color: #0A1F4E;
  }

  /* Info / warning boxes (Streamlit built-in) */
  .stAlert {
    background-color: #112B52 !important;
    border-left: 4px solid #C9A84C !important;
  }
  .stAlert p {
    color: #E0E9F5 !important;
  }

  /* Dataframe */
  .stDataFrame {
    border: 1px solid #2A4878;
    background-color: #0D264A;
  }
  .stDataFrame table {
    color: #E0E9F5;
  }
  .stDataFrame th {
    background-color: #112B52;
    color: #C9A84C;
  }
  .stDataFrame td {
    background-color: #0D264A;
    color: #E0E9F5;
  }

  /* General text */
  p, li, div:not(.stAlert):not(.stMarkdown) {
    color: #E0E9F5;
  }
  a {
    color: #7A9AD6;
  }
  hr {
    border-color: #2A4878;
  }
  /* Code blocks */
  code {
    background-color: #112B52;
    color: #E0E9F5;
  }
  /* Adjust expander */
  .streamlit-expanderHeader {
    background-color: #0D264A;
    color: #F5F0E8;
  }
  .streamlit-expanderContent {
    background-color: #0A1F4E;
  }
</style>
""", unsafe_allow_html=True)

# ── sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ StediPay")
    st.markdown("<small style='color:#B8CCE8'>Stablecoin Payment Infrastructure<br>v0.2-pilot  |  April 2026 regulatory update</small>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("Navigate", [
        "🏠  Overview",
        "💳  Payment Simulator",
        "📊  Reserve Dashboard",
        "🤖  Agent Activity Log",
        "🔄  Smart Swap Engine",
        "🛂  Travel Rule Checker",
        "⚖️   EU Regulatory Matrix",
    ])
    st.divider()
    st.markdown("<small style='color:#B8CCE8'>Portfolio project by<br><b style='color:#E8C87A'>Hasret Ozan Sevim</b><br>PhD Candidate · Researcher<br>University of Camerino and Catholic University of Sacred Heart<br><br>© 2024–2026 Hasret Ozan Sevim<br><span style='color:#8899AA'>BUSL-1.1 Licence</span></small>", unsafe_allow_html=True)
    st.markdown("<a href='https://github.com/EconoDLT/Stedipay' style='color:#7A9AD6;font-size:0.8rem'>GitHub →</a>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════════════════
if "Overview" in page:
    st.markdown("# ⚡ StediPay")
    st.markdown("### Smart Stablecoin Payments — with Smart Swap Engine")
    st.markdown("""
    <p style='color:#B8CCE8;max-width:720px'>
    StediPay enables neobanks to issue a card that settles in EURC/USDC on-chain,
    while a rules-bound AI agent automatically farms yield on idle reserves across the top audited lending protocols.
    Built for full EU regulatory compliance: MiCA, TFR zero-threshold Travel Rule, PSD3/PSR technical service provider model, DORA, and AI Act.
    </p>
    """, unsafe_allow_html=True)

    st.info("📋 **April 2026 regulatory update:** Travel Rule (TFR Reg. EU 2023/1113) in force since 30 Dec 2024 — zero threshold, all CASP-to-CASP transfers. PSD3/PSR political agreement 27 Nov 2025 — EBA Opinion (12 Feb 2026) clarifies dual authorisation. AI Act high-risk provisions apply from 2 Aug 2026.")

    st.divider()

# ── Smart Swap Diagram ─────────────────────────────────────────────
st.markdown("## 🔄 How the Smart Swap Engine Works")

st.image(
    "Stedipay_Diagram.png",
    caption="StediPay Smart Swap Engine — Euro Stablecoin Arbitrage Cashback Flow",
    use_container_width=True
)

st.markdown("""
<div style='background:#0D264A;
            border:1px solid #2A4878;
            border-left:4px solid #C9A84C;
            padding:18px 22px;
            margin-top:10px;
            margin-bottom:25px;
            color:#B8CCE8;
            line-height:1.8;'>

<b style='color:#F5F0E8'>How it works:</b><br><br>

• Customer pays <b>100 EURC</b> with the StediPay card.<br>
• Smart Swap pauses settlement for ~6–8 seconds.<br>
• StediPay scans Euro stablecoin liquidity pools (EUROe, EURCV, etc.).<br>
• If no cheaper route exists → transaction settles normally in EURC.<br>
• If another Euro stablecoin trades cheaper → StediPay executes smart swap arbitrage.<br>
• Net savings after fees are periodically cashbacked to the customer.

</div>
""", unsafe_allow_html=True)
            
    col1, col2, col3, col4, col5 = st.columns(5)
    metrics = [
        (col1, "Testnet Tx", "12,847", "+3.2%"),
        (col2, "EURC Processed", "€2.4M", "+8.1%"),
        (col3, "Avg APY (reserves)", "~4.6%", "+0.1%"),
        (col4, "Travel Rule records", "12,847", "100%"),
        (col5, "Avg Settlement", "~2s", "Polygon"),
    ]
    for col, label, val, delta in metrics:
        with col:
            st.metric(label, val, delta)

    st.divider()

    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.markdown("### Stablecoin Sandwich Architecture")
        for step, color, text in [
            ("01", "#2ECC71",  "**User** pays with StediPay card powered by a payment infrastructure service provider"),
            ("02", "#C9A84C",  "**BaaS neobank issuer** authorises (PSD3/PSR payment institution licence)"),
            ("03", "#E67E22",  "**Travel Rule Module** assembles IVMS101 originator data packet (TFR 2023/1113 — zero threshold)"),
            ("04", "#E74C3C",  "**Compliance Module** screens via a KYT model; verifies unhosted wallet if applicable (EBA/GL/2024/11 §8)"),
            ("05", "#5DBCD2",  "**AI Agent** routes to Polygon PoS (~2s, ~$0.003 gas); transmits Travel Rule packet to beneficiary CASP"),
            ("06", "#8247E5",  "**EURC transfer** executes on-chain; DORA ICT event log + CARF reporting record created"),
            ("07", "#C9A84C",  "**Idle reserves** (above 15% buffer) deployed to the top audited lending protocols at ~4–5% APY"),
            ("08", "#2ECC71",  "**70% yield** credited to user as cashback; 30% protocol revenue (yield kept separate from MiCA Art. 48 reserve)"),
        ]:
            st.markdown(f"""
            <div class='step-card'>
              <span class='step-num'>Step {step}</span> &nbsp; {text}
            </div>
            """, unsafe_allow_html=True)

    with col_b:
        st.markdown("### Tech & Compliance Stack")
        stack = {
            "Settlement": "EURC/USDC · Polygon PoS · ETH L1 (no affiliation with any issuer or network)",
            "Smart Account": "ERC-4337 (account abstraction)",
            "Yield Vault": "ERC-4626",
            "Cross-chain": "Two Multi-Chain Bridge Protocols (Primary-Fallback)",
            "Travel Rule": "TFR 2023/1113 · IVMS101",
            "AML": "KYT models",
            "AI Agent": "Rules-bound · Permission-scoped",
            "MiCA": "EURC (MiCA-authorised EMT)",
            "PSD3/PSR": "Technical service provider model",
            "DORA": "ICT TPSP · ICT risk register",
            "AI Act": "High-risk assessment in progress",
        }
        for k, v in stack.items():
            st.markdown(f"""
            <div style='margin:6px 0;'>
              <span style='color:#C9A84C;font-weight:600;font-size:0.85rem'>{k}</span><br>
              <span style='color:#A0B8D8;font-size:0.8rem;font-family:"IBM Plex Mono",monospace'>{v}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Quick Links")
        for lbl, url in [
            ("📁 GitHub Repository", "https://github.com/EconoDLT/Stedipay"),
            ("📄 Business Booklet", "https://github.com/EconoDLT/StedipayApp/blob/main/StediPay_Business_Booklet.docx"),
            ("🔗 LinkedIn", "https://www.linkedin.com/in/hasret-ozan-sevim"),
        ]:
            st.markdown(f"[{lbl}]({url})")


# ══════════════════════════════════════════════════════════════════════════
# PAYMENT SIMULATOR
# ══════════════════════════════════════════════════════════════════════════
elif "Payment Simulator" in page:
    st.markdown("# 💳 Payment Simulator")
    st.markdown("<p style='color:#B8CCE8'>Simulate a card payment through StediPay infrastructure (Polygon Amoy testnet) — includes Travel Rule data flow</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("#### Payment Parameters")
        amount = st.number_input("Payment amount (EUR)", min_value=1.0, max_value=50000.0, value=85.00, step=0.01)
        currency = st.selectbox("Stablecoin", ["EURC (MiCA-authorised)", "USDC (MiCA-authorised)"])
        network = st.selectbox("Settlement network", ["Auto (recommended)", "Polygon PoS", "Ethereum L1 (batch)"])
        merchant = st.text_input("Merchant name", value="Osteria del Turco, Milano")
        beneficiary_type = st.selectbox("Beneficiary wallet type", [
            "CASP-custodied (another licensed CASP)",
            "Unhosted / self-custodied wallet"
        ])
        yield_enabled = st.toggle("Auto-yield on remaining balance (AAVE v3)", value=True)

        if beneficiary_type == "Unhosted / self-custodied wallet":
            st.warning("⚠️ **Unhosted wallet detected.** Per EBA/GL/2024/11 §8, cryptographic proof of wallet ownership is required before settlement. Self-declaration is not sufficient.")
            wallet_verified = st.checkbox("Wallet ownership verified (cryptographic signature)", value=False)
        else:
            wallet_verified = True

        if st.button("⚡ Execute Simulated Payment", type="primary", use_container_width=True):
            if not wallet_verified and beneficiary_type == "Unhosted / self-custodied wallet":
                st.error("❌ **Settlement blocked.** Unhosted wallet ownership not verified. Required by TFR Art. 14 + EBA/GL/2024/11 §8.")
            else:
                with st.spinner("Routing through StediPay (assembling Travel Rule packet)..."):
                    time.sleep(1.5)

                tx_hash = "0x" + hashlib.sha256(f"{amount}{currency}{time.time()}".encode()).hexdigest()
                settlement_time = round(random.uniform(1.5, 2.8), 2)
                gas_usd = round(random.uniform(0.001, 0.006), 4)
                net = "Polygon PoS" if amount < 1000 else "Ethereum L1"
                tr_ref = "TR-" + hashlib.md5(tx_hash.encode()).hexdigest()[:12].upper()

                st.success("✅ Payment simulated successfully — Travel Rule packet transmitted")
                st.markdown(f"""
                <div style='background:#0D264A;border:1px solid #2A4878;border-radius:8px;padding:16px;margin-top:8px'>
                  <div style='color:#C9A84C;font-weight:700;font-size:1rem;margin-bottom:8px'>Transaction Confirmed + Travel Rule Transmitted</div>
                  <div class='tx-hash'>Tx hash: {tx_hash[:42]}...</div>
                  <br>
                  <table style='color:#E0E9F5;font-size:0.85rem;width:100%'>
                    <tr><td style='color:#B8CCE8'>Amount</td><td><b>{amount:.2f} {currency.split()[0]}</b></td></tr>
                    <tr><td style='color:#B8CCE8'>Network</td><td>{net}</td></tr>
                    <tr><td style='color:#B8CCE8'>Settlement time</td><td style='color:#C9A84C'>{settlement_time}s</td></tr>
                    <tr><td style='color:#B8CCE8'>Gas cost</td><td>${gas_usd}</td></tr>
                    <tr><td style='color:#B8CCE8'>Travel Rule ref</td><td><span class='tx-hash'>{tr_ref}</span></td></tr>
                    <tr><td style='color:#B8CCE8'>TFR Art. 14 data</td><td><span class='badge-green'>TRANSMITTED</span></td></tr>
                    <tr><td style='color:#B8CCE8'>KYC/AML check</td><td><span class='badge-green'>PASS — Chainalysis KYT</span></td></tr>
                    <tr><td style='color:#B8CCE8'>Beneficiary CASP</td><td><span class='badge-green'>TFR Art. 15 data received</span></td></tr>
                    <tr><td style='color:#B8CCE8'>DORA event log</td><td><span class='badge-teal'>RECORDED</span></td></tr>
                    <tr><td style='color:#B8CCE8'>CARF record</td><td><span class='badge-teal'>CREATED</span></td></tr>
                    <tr><td style='color:#B8CCE8'>Yield re-deployed</td><td><span class='badge-gold'>{'Yes → AAVE v3 (~4.8% APY)' if yield_enabled else 'Disabled'}</span></td></tr>
                   </table>
                </div>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### Payment Route — Stablecoin Sandwich Flow")

        labels = ["Card Terminal", "Neobank BaaS (PSD3)", "StediPay SDK", "Travel Rule Module",
                  "AI Agent", "Polygon PoS", "EURC Transfer", "Merchant CASP", "Treasury Vault", "User Balance"]
        source = [0, 1, 2, 2, 3, 4, 5, 6, 4]
        target = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        value  = [100, 100, 100, 100, 90, 90, 90, 81, 9]

        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15, thickness=20,
                label=labels,
                color=["#C9A84C","#1B2A4A","#0E7C7B","#E67E22","#C9A84C",
                       "#8247E5","#627EEA","#2ECC71","#E67E22","#5DBCD2"]
            ),
            link=dict(source=source, target=target, value=value,
                      color=["rgba(201,168,76,0.2)"]*len(source))
        ))
        fig.update_layout(
            paper_bgcolor="#0A1F4E", plot_bgcolor="#0D264A", font_color="#E0E9F5", font_size=11,
            margin=dict(l=10,r=10,t=10,b=10), height=380
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Agent + Travel Rule Decision Log (simulated)")
        tx_hash_short = "0x" + hashlib.sha256(f"{amount}{time.time()}".encode()).hexdigest()[:20]
        logs = [
            ("00:00:000", "PAYMENT_MODULE",      f"Auth request received: €{amount:.2f} {currency.split()[0]}", "INFO"),
            ("00:00:030", "TRAVEL_RULE_MODULE",  "Assembling IVMS101 originator data packet (TFR Art. 14)", "INFO"),
            ("00:00:044", "COMPLIANCE_MODULE",   "KYT: merchant wallet risk score 2/100 — PASS", "PASS"),
            ("00:00:058", "TRAVEL_RULE_MODULE",  f"Originator data: name, DLT address, postal address — complete", "INFO"),
            ("00:00:089", "PAYMENT_MODULE",      f"Reserve buffer: 16.1% > 15% threshold — OK", "INFO"),
            ("00:00:134", "PAYMENT_MODULE",      f"Route: Polygon PoS (gas: ${random.uniform(0.001,0.005):.4f}) — selected", "INFO"),
            ("00:00:912", "PAYMENT_MODULE",      f"EURC transfer submitted: {tx_hash_short}...", "INFO"),
            ("00:01:050", "TRAVEL_RULE_MODULE",  "TFR data packet transmitted to beneficiary CASP (IVMS101)", "CONFIRM"),
            ("00:01:487", "PAYMENT_MODULE",      "On-chain confirmation: block 61,204,871", "CONFIRM"),
            ("00:01:500", "DORA_MODULE",         "ICT event logged (DORA Art. 17 — non-major incident)", "INFO"),
            ("00:01:508", "CARF_MODULE",         "CARF reporting record created (user account ref)", "INFO"),
            ("00:01:515", "YIELD_MODULE",        "Residual 85% → Vault deposit: ~4.8% APY", "INFO"),
        ]
        for ts, module, msg, typ in logs:
            color = {"INFO":"#B8CCE8","PASS":"#2ECC71","CONFIRM":"#C9A84C"}.get(typ,"#B8CCE8")
            st.markdown(f"""
            <div style='font-family:"IBM Plex Mono",monospace;font-size:0.73rem;
                        padding:3px 0;border-bottom:1px solid #2A4878'>
              <span style='color:#7A9AD6'>{ts}</span>
              <span style='color:{color};margin:0 8px'>[{module}]</span>
              <span style='color:#D0DCF0'>{msg}</span>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# RESERVE DASHBOARD
# ══════════════════════════════════════════════════════════════════════════
elif "Reserve Dashboard" in page:
    st.markdown("# 📊 Reserve Dashboard")
    st.markdown("<p style='color:#B8CCE8'>Yield strategy allocation and performance. Yield reserves kept strictly separate from MiCA Art. 48 regulatory reserve (simulated data).</p>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total AUM (EURC)", "€2,847,200", "+€124,300")
    with col2: st.metric("Blended APY", "~4.6%", "+0.1%")
    with col3: st.metric("30-Day Yield", "€10,841", "+8.3%")
    with col4: st.metric("Liquidity Buffer", "16.1%", "+0.1% (target: 15%)")

    st.info("ℹ️ **MiCA Art. 48 note:** The yield farming reserves shown here represent the infrastructure layer's operating float, kept strictly separate from the EMT issuer's regulatory reserve which must be held in low-risk, segregated assets per MiCA Title IV.")

    st.divider()
    col_l, col_r = st.columns([2, 3])

    with col_l:
        st.markdown("#### Reserve Allocation")
        protocols = ["AAVE v3 (50%)", "Spark Protocol (20%)", "Uniswap v4 LP (15%)", "Liquidity Buffer (15%)"]
        allocs    = [50, 20, 15, 15]
        apys      = [4.82, 5.20, 3.10, 0.0]
        colors_p  = ["#627EEA", "#E67E22", "#8247E5", "#5DBCD2"]

        fig_donut = go.Figure(go.Pie(
            labels=[f"{p}<br>APY: {a:.2f}%" for p,a in zip(protocols,apys)],
            values=allocs,
            hole=0.6,
            marker_colors=colors_p,
            textfont_size=11,
            textfont_color="#E0E9F5"
        ))
        fig_donut.update_layout(
            paper_bgcolor="#0A1F4E", font_color="#E0E9F5",
            showlegend=True, legend_font_size=10,
            margin=dict(l=0,r=0,t=0,b=0), height=300,
            annotations=[dict(text="~4.6%<br>blended", x=0.5, y=0.5,
                              font_size=14, font_color="#C9A84C", showarrow=False)]
        )
        st.plotly_chart(fig_donut, use_container_width=True)

        for p, a, al, c in zip(protocols, apys, allocs, colors_p):
            usd = 2847200 * al / 100
            st.markdown(f"""
            <div style='display:flex;justify-content:space-between;align-items:center;
                        background:#0D264A;border-radius:6px;padding:8px 12px;margin:4px 0;
                        border-left:3px solid {c}'>
              <div>
                <div style='color:#F5F0E8;font-size:0.85rem;font-weight:600'>{p}</div>
                <div style='color:#B8CCE8;font-size:0.75rem'>€{usd:,.0f} deployed</div>
              </div>
              <div style='color:#C9A84C;font-weight:700;font-size:1rem'>{a:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

    with col_r:
        st.markdown("#### 30-Day Cumulative Yield Performance")
        dates = pd.date_range(end=datetime.today(), periods=30, freq="D")
        np.random.seed(42)
        daily = np.random.normal(350, 45, 30)
        cumulative = np.cumsum(daily)

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=dates, y=cumulative, mode="lines", name="Cumulative yield",
            line=dict(color="#C9A84C", width=2.5),
            fill="tozeroy", fillcolor="rgba(201,168,76,0.1)"
        ))
        fig_line.add_trace(go.Bar(
            x=dates, y=daily, name="Daily yield (EUR)",
            marker_color="#0E7C7B", opacity=0.6, yaxis="y2"
        ))
        fig_line.update_layout(
            paper_bgcolor="#0A1F4E", plot_bgcolor="#0D264A", font_color="#E0E9F5", height=280,
            xaxis=dict(gridcolor="#2A4878", title_font_color="#C9A84C"),
            yaxis=dict(title="Cumulative EUR", gridcolor="#2A4878", title_font_color="#C9A84C"),
            yaxis2=dict(title="Daily EUR", overlaying="y", side="right", title_font_color="#0E7C7B"),
            legend=dict(bgcolor="#0A1F4E", font_size=10),
            margin=dict(l=10,r=10,t=10,b=10)
        )
        st.plotly_chart(fig_line, use_container_width=True)

        st.markdown("#### AI Agent Rebalancing History (last 7 days)")
        rebalance_data = {
            "Date": pd.date_range(end=datetime.today(), periods=7, freq="D").strftime("%b %d"),
            "Action": ["No change","AAVE→Spark (+5%)","No change","Uniswap→AAVE (+3%)","No change","Buffer refill","No change"],
            "Trigger": ["APY stable","Spark APY spike +0.6%","APY stable","Uniswap IL > threshold","APY stable","Buffer < 15%","APY stable"],
            "Net APY Δ": ["+0.00%","+0.11%","+0.00%","+0.07%","+0.00%","+0.00%","+0.00%"],
        }
        st.dataframe(pd.DataFrame(rebalance_data), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════
# AGENT ACTIVITY LOG
# ══════════════════════════════════════════════════════════════════════════
elif "Agent Activity" in page:
    st.markdown("# 🤖 AI Agent Activity Log")
    st.markdown("<p style='color:#B8CCE8'>Rules-bound agent invocations — last 100 actions (Polygon Amoy testnet). All modules operate within permission-scoped boundaries encoded in StediPayRegistry.</p>", unsafe_allow_html=True)

    st.warning("⚠️ **AI Act note:** The StediPay AI Agent is classified as a likely **high-risk AI system (Annex III §5(b))** due to its autonomous financial decisions. Conformity assessment, human oversight mechanism, and EU AI database registration are required before commercial deployment (deadline: 2 Aug 2026). This testnet demo operates under human review at all stages.")

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Actions (24h)", "847", "+12%")
    with col2: st.metric("Travel Rule records", "623", "100% coverage")
    with col3: st.metric("Yield rebalances", "14", "+2")
    with col4: st.metric("Compliance blocks", "3", "-1")

    st.divider()

    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.markdown("#### Module Invocations (24h)")
        modules = ["Payment Module","Travel Rule Module","Compliance Module","Yield Module","Bridge Module","Reserve Module","Off-Ramp Module"]
        counts  = [623, 623, 847, 89, 12, 14, 8]
        colors_m = ["#C9A84C","#E67E22","#8247E5","#E67E22","#0E7C7B","#627EEA","#2ECC71"]
        fig_bar = go.Figure(go.Bar(x=counts, y=modules, orientation="h", marker_color=colors_m, opacity=0.85))
        fig_bar.update_layout(
            paper_bgcolor="#0A1F4E", plot_bgcolor="#0D264A", font_color="#E0E9F5", height=300,
            xaxis=dict(gridcolor="#2A4878"), yaxis=dict(gridcolor="#2A4878"),
            margin=dict(l=0,r=10,t=0,b=0)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_r:
        st.markdown("#### Recent Agent Actions")
        np.random.seed(99)
        module_opts = ["PAYMENT_MODULE","TRAVEL_RULE_MODULE","COMPLIANCE_MODULE","YIELD_MODULE","BRIDGE_MODULE","RESERVE_MODULE"]
        action_opts = [
            "EURC transfer executed: €{:.2f} — TFR packet transmitted",
            "IVMS101 originator data assembled for transfer €{:.2f}",
            "KYT check PASS: wallet risk score {:.0f}/100",
            "AAVE v3 deposit: €{:.0f} EURC at ~4.8% APY",
            "Bridge route selected: ETH→Polygon (latency {}ms)",
            "Buffer rebalance: {:.1f}% → 15.0%",
        ]
        status_opts = ["CONFIRMED","TRANSMITTED","PASS","CONFIRMED","CONFIRMED","COMPLETED"]
        color_opts  = ["#C9A84C","#E67E22","#2ECC71","#E67E22","#0E7C7B","#5DBCD2"]

        rows = ""
        for i in range(12):
            mod_i = random.randint(0,5)
            mod = module_opts[mod_i]
            val = random.uniform(5,500) if mod_i in [0,1] else random.uniform(2,15) if mod_i==2 else random.uniform(100,5000)
            act = action_opts[mod_i].format(val if mod_i<=2 else (val if mod_i==3 else (int(random.uniform(50,200)) if mod_i==4 else val)))
            ts  = (datetime.now() - timedelta(minutes=random.randint(1,240))).strftime("%H:%M:%S")
            status = status_opts[mod_i]
            c = color_opts[mod_i]
            tx = f"0x{random.randint(10**38,10**39):x}"[:18]+"..."
            rows += f"""
            <tr style='border-bottom:1px solid #2A4878'>
              <td style='color:#B8CCE8;font-family:"IBM Plex Mono",monospace;font-size:0.72rem;padding:5px 4px'>{ts}</td>
              <td style='font-size:0.75rem;padding:5px 4px'><span style='color:{c};font-weight:600'>{mod}</span></td>
              <td style='color:#E0E9F5;font-size:0.75rem;padding:5px 4px'>{act}</td>
              <td style='padding:5px 4px'><span style='background:{c}22;color:{c};padding:2px 7px;border-radius:10px;font-size:0.7rem'>{status}</span></td>
              <td style='color:#7A9AD6;font-family:"IBM Plex Mono",monospace;font-size:0.68rem;padding:5px 4px'>{tx}</td>
            </tr>
            """
        st.markdown(f"""
        <table style='width:100%;border-collapse:collapse;background:#0D264A'>
          <thead>
            <tr style='color:#C9A84C;font-size:0.75rem;text-transform:uppercase'>
              <th style='text-align:left;padding:6px 4px'>Time</th>
              <th style='text-align:left;padding:6px 4px'>Module</th>
              <th style='text-align:left;padding:6px 4px'>Action</th>
              <th style='text-align:left;padding:6px 4px'>Status</th>
              <th style='text-align:left;padding:6px 4px'>Tx Hash</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# SMART SWAP ENGINE
# ══════════════════════════════════════════════════════════════════════════
elif "Smart Swap" in page:
    st.markdown("# 🔄 Smart Swap Engine")
    st.markdown("<p style='color:#B8CCE8'>Real-time EMT price scan and best-execution swap at point of payment. MiCA Art. 78 compliant. Simulated data — April 2026.</p>", unsafe_allow_html=True)

    st.info("**Legal basis:** The Smart Swap Engine is structured as a **best-execution service** under MiCA Art. 78, not yield on EMT holdings (prohibited under MiCA Art. 40/50). The engine generates a price improvement on an active transaction, not interest paid for holding time. Only MiCA-authorised EMTs from the ESMA registry are used.")

    st.divider()
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### Simulate a Smart Swap")
        payment_emt = st.selectbox("Your current EMT", ["EURC (Circle Europe)", "EUROe (Membrane Finance)", "EURCV (SG-Forge)"])
        payment_amount = st.number_input("Payment amount (EUR)", min_value=1.0, max_value=10000.0, value=150.00, step=1.0)
        st.markdown("**Your trusted issuer whitelist:**")
        use_eurc   = st.checkbox("EURC — Circle Europe (EMI, France)", value=True)
        use_euroe  = st.checkbox("EUROe — Membrane Finance (EMI, Finland)", value=True)
        use_eurcv  = st.checkbox("EURCV — Société Générale-Forge (Credit inst., France)", value=True)
        use_eurq   = st.checkbox("EURQ — Quantoz Payments (EMI, Netherlands)", value=False)
        min_spread = st.slider("Min. spread threshold (bps)", min_value=3, max_value=20, value=5, help="Swap only triggered if spread exceeds this threshold (covers gas costs). 1 bps = 0.01%")
        run_swap   = st.button("⚡ Run Smart Swap Simulation", type="primary", use_container_width=True)

    with col2:
        if run_swap:
            import time as _time
            import random as _random
            import hashlib as _hashlib

            whitelist = []
            if use_eurc:  whitelist.append("EURC")
            if use_euroe: whitelist.append("EUROe")
            if use_eurcv: whitelist.append("EURCV")
            if use_eurq:  whitelist.append("EURQ")

            if len(whitelist) < 2:
                st.warning("Enable at least 2 EMTs in your whitelist for the Swap Engine to scan pairs.")
            else:
                with st.spinner("Scanning whitelisted EMT pools on Polygon PoS..."):
                    _time.sleep(1.2)

                _random.seed(int(payment_amount * 100))
                pool_prices = {t: 1.0 + _random.uniform(-0.0025, 0.0025) for t in whitelist}
                current_emt = payment_emt.split()[0]
                if current_emt not in pool_prices:
                    pool_prices[current_emt] = 1.0

                best_token = max(pool_prices, key=pool_prices.get)
                best_price = pool_prices[best_token]
                current_price = pool_prices.get(current_emt, 1.0)
                spread_bps = int((best_price - current_price) * 10000)
                gas_cost_eur = _random.uniform(0.002, 0.008)
                net_cashback = max(0.0, (best_price - current_price) * payment_amount * 0.8 - gas_cost_eur)
                swap_executed = spread_bps >= min_spread and net_cashback > 0
                tx_hash = "0x" + _hashlib.sha256(f"{payment_amount}{best_token}{_time.time()}".encode()).hexdigest()[:20]

                st.markdown("#### Pool Price Scan Results")
                import pandas as _pd
                rows = []
                for t, p in pool_prices.items():
                    sp = int((p - current_price) * 10000)
                    rows.append({"EMT": t, "Pool Price (EUR)": f"{p:.6f}", "Spread vs current (bps)": sp, "Selected": "✓" if t == best_token and swap_executed else ""})
                st.dataframe(_pd.DataFrame(rows), use_container_width=True, hide_index=True)

                if swap_executed:
                    st.success(f"✅ Swap executed — {current_emt} → {best_token} — Cashback: **€{net_cashback:.4f}**")
                    st.markdown(f"""
                    <div style='background:#0D264A;border:1px solid #2A4878;padding:16px;margin-top:8px'>
                      <table style='color:#E0E9F5;font-size:0.85rem;width:100%'>
                        <tr><td style='color:#B8CCE8'>EMT swapped</td><td><b>{current_emt} → {best_token}</b></td></tr>
                        <tr><td style='color:#B8CCE8'>Spread captured</td><td><b>{spread_bps} bps ({spread_bps/100:.2f}%)</b></td></tr>
                        <tr><td style='color:#B8CCE8'>Gross gain</td><td>€{(best_price-current_price)*payment_amount:.4f}</td></tr>
                        <tr><td style='color:#B8CCE8'>Gas cost</td><td>€{gas_cost_eur:.4f}</td></tr>
                        <tr><td style='color:#B8CCE8'>User cashback (80%)</td><td style='color:#C9A84C'><b>€{net_cashback:.4f}</b></td></tr>
                        <tr><td style='color:#B8CCE8'>Protocol (20%)</td><td>€{net_cashback*0.25:.4f}</td></tr>
                        <tr><td style='color:#B8CCE8'>Legal basis</td><td>MiCA Art. 78 best-execution</td></tr>
                        <tr><td style='color:#B8CCE8'>Tx hash</td><td style='font-family:monospace;font-size:0.72rem'>{tx_hash}...</td></tr>
                       </table>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    reason = "spread below threshold" if spread_bps < min_spread else "net cashback negative after gas"
                    st.info(f"ℹ️ No swap executed ({reason}). Payment proceeds in {current_emt} — no loss, no action.")

                st.markdown("#### Legal compliance check")
                checks = [
                    ("MiCA Art. 78 best-execution", "Engine scanned all whitelisted pools and selected best available price", "PASS"),
                    ("MiCA Art. 40/50 — no interest", "Gain is a transaction price improvement, not time-based interest on balance", "PASS"),
                    ("MiCA Art. 76 — market integrity", "Used open market pool prices only; no manipulation", "PASS"),
                    ("MiCA Art. 45 — authorised EMTs only", f"All tokens in whitelist are MiCA-authorised EMTs from ESMA registry", "PASS"),
                    ("TFR intra-account swap", "Swap is intra-account (no CASP-to-CASP transfer) — TFR Travel Rule not triggered by swap", "PASS"),
                    ("Atomic revert protection", "Swap contract coded to revert if any step is loss-making", "PASS"),
                ]
                for label, detail, status in checks:
                    color = "#5CD99A" if status == "PASS" else "#E08080"
                    bg = "#0D264A"
                    st.markdown(f"""
                    <div style='background:{bg};border-left:3px solid {color};padding:8px 14px;margin:4px 0'>
                      <span style='color:{color};font-weight:600;font-size:0.82rem'>{status}</span>
                      <span style='color:#E0E9F5;font-size:0.82rem;margin-left:10px'>{label}</span>
                      <div style='color:#B8CCE8;font-size:0.76rem;margin-top:2px'>{detail}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background:#0D264A;padding:32px;text-align:center;margin-top:40px;border:1px solid #2A4878'>
              <div style='font-size:1.5rem;color:#C9A84C;margin-bottom:10px'>🔄</div>
              <div style='color:#B8CCE8;font-size:0.95rem'>Configure your whitelist and click <b>Run Smart Swap Simulation</b> to see the engine in action.</div>
              <div style='color:#8899AA;font-size:0.82rem;margin-top:12px'>The engine scans live pool prices across Uniswap v4 and Curve,<br>selects the best EMT, and credits the spread surplus as cashback.</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# TRAVEL RULE CHECKER
# ══════════════════════════════════════════════════════════════════════════
elif "Travel Rule" in page:
    st.markdown("# 🛂 Travel Rule Compliance Checker")
    st.markdown("<p style='color:#B8CCE8'>EU Transfer of Funds Regulation (Reg. EU 2023/1113) — in force since 30 Dec 2024 — zero threshold, all CASP-to-CASP transfers. Analysis by Hasret Ozan Sevim.</p>", unsafe_allow_html=True)

    st.info("**Key fact:** The EU Travel Rule (TFR) has **no de minimis threshold**. Unlike FATF's €1,000 standard, every crypto-asset transfer between CASPs in the EU — regardless of amount — must carry full originator and beneficiary data.")

    col1, col2 = st.columns([1, 1])
    with col1:
        transfer_type = st.selectbox("Transfer type", [
            "EURC card payment → merchant CASP wallet",
            "EURC payment → unhosted (self-custodied) wallet",
            "USDC bridge: Polygon → Ethereum L1",
            "EURC off-ramp → bank account (fiat)",
            "EURC yield withdrawal from AAVE v3",
            "Cross-border EURC transfer → third-country CASP",
            "EURC batch settlement → acquiring bank",
        ])
        amount_tr = st.number_input("Transfer amount (EUR)", min_value=0.01, max_value=1000000.0, value=85.00, step=0.01)
        entity = st.selectbox("StediPay entity role", [
            "Originating CASP",
            "Beneficiary CASP",
            "Intermediary CASP",
            "Technical service provider (not a CASP)",
        ])
        run = st.button("🔍 Analyse Travel Rule Obligations", type="primary", use_container_width=True)

    with col2:
        if run:
            st.markdown(f"#### Travel Rule Analysis: _{transfer_type}_")
            st.markdown(f"**Amount:** €{amount_tr:.2f}  |  **Role:** {entity}")

            threshold_note = "✅ TFR EU: **zero threshold** — obligations apply regardless of amount."
            st.success(threshold_note)

            analyses = {
                "EURC card payment → merchant CASP wallet": {
                    "TFR obligation": ("green", "FULL", "Full originator data (TFR Art. 14) + beneficiary data (Art. 15) required. Transmit IVMS101 packet to beneficiary CASP simultaneously with EURC transfer."),
                    "Originator data": ("green", "REQUIRED", "Full legal name, DLT address, crypto-asset account number, postal address (or national ID/DOB/LEI)."),
                    "Beneficiary data": ("green", "REQUIRED", "Full legal name, DLT address, crypto-asset account number."),
                    "Unhosted wallet": ("green", "N/A", "Merchant uses a CASP-custodied wallet — no unhosted wallet verification required."),
                    "Intermediary CASP": ("green", "FORWARD", "Any intermediary CASP (Art. 16) must forward all TFR data without modification."),
                },
                "EURC payment → unhosted (self-custodied) wallet": {
                    "TFR obligation": ("orange", "ENHANCED", "Full originator data required. Beneficiary is unhosted wallet — enhanced due diligence per EBA/GL/2024/11 §8."),
                    "Originator data": ("green", "REQUIRED", "Full legal name, DLT address, crypto-asset account number, postal address."),
                    "Wallet verification": ("orange", "REQUIRED", "Must verify customer controls the unhosted address. Self-declaration NOT sufficient (FMA Austria guidance, Dec 2025). Use: cryptographic signature, micro-transfer, or other suitable technical means per EBA/GL/2024/11 §83."),
                    "Risk assessment": ("orange", "ENHANCED", "Risk-based assessment required for unhosted wallet transactions. Higher-risk indicators require enhanced monitoring."),
                    "Data transmission": ("yellow", "LIMITED", "No TFR data packet transmitted to unhosted wallet (no counterparty CASP). Originator CASP retains records internally."),
                },
                "USDC bridge: Polygon → Ethereum L1": {
                    "TFR obligation": ("green", "FULL", "Cross-chain bridge treated as crypto-asset transfer. Travel Rule data must travel with a cross-chain message."),
                    "Intermediary CASP": ("green", "APPLIES", "The bridge protocol acts as technical messaging layer; StediPay as intermediary CASP (Art. 16) must ensure data is not stripped in transit."),
                    "Originator data": ("green", "TRANSMITTED", "IVMS101 packet embedded in the cross-chain message payload alongside USDC transfer."),
                    "Bridge-specific": ("yellow", "NOTE", "TFR Art. 16(3): intermediary CASPs must forward all information received. Technical limitations (transit encoding) have a transitional window per EBA/GL/2024/11 §24."),
                },
                "Cross-border EURC transfer → third-country CASP": {
                    "TFR obligation": ("orange", "ENHANCED EDD", "Third-country CASP transfer triggers enhanced due diligence (TFR Art. 19). Assess whether counterparty CASP is in a non-equivalent jurisdiction."),
                    "EDD measures": ("orange", "REQUIRED", "Implement EDD on third-country counterparty CASPs per TFR Art. 19. Assess AML/CFT framework equivalence. Higher risk if counterparty is in FATF high-risk or monitored jurisdiction."),
                    "Data completeness": ("orange", "VERIFY", "Confirm counterparty CASP can receive and process IVMS101 Travel Rule data. Many non-EU CASPs are not yet Travel Rule compliant — document reasonable steps taken."),
                    "FATF comparison": ("yellow", "NOTE", "FATF Travel Rule threshold: USD/EUR 1,000. EU TFR: zero threshold. Counterparty in FATF-only jurisdiction may not transmit data for sub-€1,000 transfers — manage as incoming incomplete data per EBA/GL/2024/11 §4."),
                },
            }

            default_analysis = {
                "TFR obligation": ("yellow", "REVIEW REQUIRED", "Transfer type requires case-by-case analysis under TFR Reg. EU 2023/1113. EU zero-threshold applies — full originator and beneficiary data required for all CASP-to-CASP transfers."),
                "Originator data (Art. 14)": ("yellow", "REQUIRED", "Name, DLT address, account number, and postal address/national ID/DOB/LEI."),
                "Beneficiary data (Art. 15)": ("yellow", "REQUIRED", "Name, DLT address, account number."),
                "Record retention": ("green", "5 YEARS", "All TFR data must be retained for 5 years per AML Directive requirements."),
            }

            result = analyses.get(transfer_type, default_analysis)

            color_map = {"green":"#0a2a0a|#2ECC71", "yellow":"#2a1f00|#C9A84C", "orange":"#2a1000|#E67E22", "red":"#2a0a0a|#E74C3C"}
            for label_key, (risk, badge, desc) in result.items():
                bg, fc = color_map.get(risk, "2a1f00|C9A84C").split("|")
                st.markdown(f"""
                <div style='background:#{bg};border-left:4px solid #{fc};
                            padding:12px 16px;margin:8px 0'>
                  <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:6px'>
                    <span style='color:#{fc};font-weight:700;font-size:0.95rem'>{label_key}</span>
                    <span style='background:#{fc}33;color:#{fc};padding:2px 10px;
                                 border-radius:12px;font-size:0.75rem;font-weight:600'>{badge}</span>
                  </div>
                  <div style='color:#CCC;font-size:0.82rem;line-height:1.5'>{desc}</div>
                </div>
                """, unsafe_allow_html=True)

            st.warning("⚠️ This tool provides informational analysis only. It does not constitute legal advice. Regulatory analysis by Hasret Ozan Sevim.")
        else:
            st.markdown("""
            <div style='background:#0D264A;border-radius:10px;padding:24px;text-align:center;margin-top:40px;border:1px solid #2A4878'>
              <div style='font-size:2rem;margin-bottom:8px'>🛂</div>
              <div style='color:#B8CCE8'>Select a transfer type and entity role,<br>then click Analyse to get the Travel Rule obligations.</div>
              <br>
              <div style='color:#8899AA;font-size:0.8rem'>Covers: TFR Reg. EU 2023/1113 · EBA/GL/2024/11 · FATF Rec. 15/16<br>In force since 30 Dec 2024 · Zero threshold · No de minimis</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# EU REGULATORY MATRIX
# ══════════════════════════════════════════════════════════════════════════
elif "Regulatory Matrix" in page:
    st.markdown("# ⚖️ EU Regulatory Matrix")
    st.markdown("<p style='color:#B8CCE8'>Complete EU regulatory landscape for stablecoin payment infrastructure — April 2026. Analysis by Hasret Ozan Sevim.</p>", unsafe_allow_html=True)

    regs = [
        {
            "name": "MiCA (Reg. EU 2023/1114)",
            "status": "🟢 IN FORCE",
            "status_color": "#2ECC71",
            "since": "CASP rules: 30 Dec 2024. Transitional periods expire: 1 Jul 2026",
            "stedipay": "EURC (Circle Europe) and USDC (Circle) are MiCA-authorised EMTs. BaaS partner holds EMT issuer + CASP authorisation. StediPay operates as technical service provider. CASP licence pathway documented.",
            "key_obligation": "EMT issuers: Art. 48 reserves (low-risk, segregated). CASPs: white paper, governance, AML/Travel Rule, prudential requirements.",
            "gap": "CASP authorisation application required for StediPay if not relying fully on BaaS partner's licence.",
            "risk": "green",
        },
        {
            "name": "TFR / Travel Rule (Reg. EU 2023/1113)",
            "status": "🟢 IN FORCE",
            "status_color": "#2ECC71",
            "since": "30 Dec 2024 — no transitional period, no de minimis threshold",
            "stedipay": "Implemented: zero-threshold IVMS101 Travel Rule on all CASP-to-CASP transfers. Unhosted wallet verification per EBA/GL/2024/11 §8. Travel Rule packet travels with the cross-chain messages.",
            "key_obligation": "Art. 14: originator data (name, DLT address, postal address). Art. 15: beneficiary data. Art. 16: intermediary forwarding. Art. 19: third-country EDD. No minimum threshold.",
            "gap": "Interoperability with non-EU CASPs not yet Travel Rule compliant. Manage as incomplete data per EBA/GL/2024/11 §4.",
            "risk": "green",
        },
        {
            "name": "PSD3 / PSR",
            "status": "🟡 AGREED — APPLYING ~LATE 2027",
            "status_color": "#C9A84C",
            "since": "Political agreement: 27 Nov 2025. Formal adoption: ~Q2 2026. Applies: ~21 months post-adoption (~late 2027)",
            "stedipay": "EBA Opinion (12 Feb 2026): EMT transfer services require PSD2/PSD3 authorisation from 2 Mar 2026. StediPay's BaaS partner model (partner holds PSP/EMI licence) mitigates dual-auth risk. PSD3 introduces simplified CASP→PSP authorisation pathway.",
            "key_obligation": "PSR: directly applicable. PSD3: requires national transposition (18 months). Strong customer authentication. Fraud liability. Confirmation of payee. Open banking.",
            "gap": "BaaS partner must obtain PSD3/PSR payment institution licence. StediPay must ensure contracts reflect technical service provider status under PSR Art. 2.",
            "risk": "yellow",
        },
        {
            "name": "DORA (Reg. EU 2022/2554)",
            "status": "🟢 IN FORCE",
            "status_color": "#2ECC71",
            "since": "17 Jan 2025",
            "stedipay": "StediPay classified as critical ICT third-party service provider (TPSP). ICT risk register, incident classification, resilience testing documented. DORA contractual clauses for all sub-processors including LLM inference providers.",
            "key_obligation": "Art. 28–44: contractual obligations for ICT TPSPs. Incident reporting: major incidents within 4h (initial), 24h (intermediate), 1 month (final). Annual resilience testing. Register of ICT contracts.",
            "gap": "Full DORA resilience testing programme (TLPT) required before commercial deployment. LLM provider (OpenAI/Meta) must accept DORA contractual clauses.",
            "risk": "green",
        },
        {
            "name": "AI Act (Reg. EU 2024/1689)",
            "status": "🟠 IN FORCE — HIGH-RISK PROVISIONS 2 AUG 2026",
            "status_color": "#E67E22",
            "since": "In force: 1 Aug 2024. High-risk AI provisions: 2 Aug 2026",
            "stedipay": "AI Agent performing autonomous card payment routing and reserve management: likely HIGH-RISK AI (Annex III §5(b) — AI in financial services). Conformity assessment in progress. Human oversight mechanism designed. EU AI database registration required.",
            "key_obligation": "Annex III high-risk: conformity assessment, technical documentation, human oversight, accuracy/robustness/cybersecurity requirements, EU AI database registration before commercial deployment.",
            "gap": "Conformity assessment must be completed before 2 Aug 2026 for any commercial deployment. Human-in-the-loop mechanism must be operational and documented.",
            "risk": "orange",
        },
        {
            "name": "AMLA",
            "status": "🟡 OPERATIONAL — DIRECT SUPERVISION FROM 2026",
            "status_color": "#C9A84C",
            "since": "AMLA operational: 1 Jul 2025. Direct supervision of large cross-border CASPs: 2026",
            "stedipay": "Readiness checklist maintained. Enhanced CDD, transaction monitoring, and AML/CFT reporting architecture supports AMLA standards. AML policy documentation follows AMLA draft RTS from 2025 consultation.",
            "key_obligation": "AMLA will directly supervise largest cross-border CASPs for AML/CFT. National FIUs remain primary for most firms. AMLA sets harmonised AML/CFT standards across EU.",
            "gap": "AMLA direct supervision framework still being finalised. Monitor AMLA RTS publications.",
            "risk": "yellow",
        },
        {
            "name": "GDPR (Reg. EU 2016/679)",
            "status": "🟢 ONGOING",
            "status_color": "#2ECC71",
            "since": "Ongoing — applies to all personal data processing",
            "stedipay": "Legal basis: Art. 6(1)(c) for KYC/AML. Wallet addresses = pseudonymous personal data (EDPB guidance). Privacy-by-design. TFR data sharing with counterparty CASPs requires appropriate safeguards for third-country transfers.",
            "key_obligation": "Data minimisation, retention limits, privacy by design, DPA notification for breaches within 72h. DPIA for high-risk processing (AI Agent, KYC profiling).",
            "gap": "EDPB guidance on on-chain data continues to evolve. Data Processing Agreements needed with all sub-processors.",
            "risk": "green",
        },
        {
            "name": "CARF (Crypto-Asset Reporting Framework)",
            "status": "🟡 EU IMPLEMENTING LEGISLATION 2026–2027",
            "status_color": "#C9A84C",
            "since": "OECD CARF adopted; EU implementation targeting 2026–2027; first data exchanges 2027",
            "stedipay": "CARF reporting hooks built into every transaction record from day one. Per-user annual reporting data exportable. Designed to support first CARF information exchanges by 2027.",
            "key_obligation": "Crypto-asset service providers must report user transaction data to tax authorities annually. Covers exchanges, transfers, and payments above reportable thresholds.",
            "gap": "EU implementing legislation not yet finalised. Monitor EU directive adoption timeline.",
            "risk": "yellow",
        },
    ]

    for reg in regs:
        risk_colors = {"green": "#2ECC71", "yellow": "#C9A84C", "orange": "#E67E22", "red": "#E74C3C"}
        bg_colors   = {"green": "#0a2a0a", "yellow": "#2a1f00", "orange": "#2a1000", "red": "#2a0a0a"}
        fc = risk_colors.get(reg["risk"], "#C9A84C")
        bg = bg_colors.get(reg["risk"], "#2a1f00")

        with st.expander(f"{reg['status']}  ·  {reg['name']}", expanded=False):
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.markdown(f"**In force / timeline:** {reg['since']}")
                st.markdown(f"**Key obligation:** {reg['key_obligation']}")
            with col_b:
                st.markdown(f"**StediPay posture:** {reg['stedipay']}")
                st.markdown(f"""
                <div style='background:#{bg.replace("#","")};border-left:3px solid {fc};
                            border-radius:6px;padding:10px;margin-top:8px'>
                  <span style='color:#8899AA;font-size:0.8rem'>Open gap / dependency: </span>
                  <span style='color:#CCC;font-size:0.82rem'>{reg['gap']}</span>
                </div>
                """, unsafe_allow_html=True)

    st.divider()
    st.warning("⚠️ This matrix provides informational classification only. It does not constitute legal advice. Regulatory analysis by Hasret Ozan Sevim.")
