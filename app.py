import streamlit as st
from src.data_processing import load_transactions, calculate_cashflow_metrics
from src.scoring import calculate_credit_score


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Kynthera Funds MVP",
    layout="wide"
)


# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    /* Main page */
    .stApp {
        background-color: #ffffff;
        color: #0b0f19;
    }

    /* Blue top banner */
    .hero-card {
        padding: 30px;
        border-radius: 20px;
        background: linear-gradient(135deg, #0b1f4d 0%, #155eef 100%);
        color: white;
        margin-bottom: 28px;
        box-shadow: 0 8px 22px rgba(11, 31, 77, 0.18);
    }

    .hero-card h1 {
        color: white;
        font-size: 42px;
        margin-bottom: 6px;
        font-weight: 850;
    }

    .hero-card p {
        color: #e5edff;
        font-size: 18px;
        margin-bottom: 0px;
    }

    /* General cards */
    .section-card {
        padding: 24px;
        border-radius: 18px;
        background-color: #ffffff;
        border: 1px solid #dbe3f0;
        box-shadow: 0 4px 14px rgba(11, 31, 77, 0.08);
        margin-bottom: 20px;
    }

    /* Score card */
    .score-card {
        padding: 30px;
        border-radius: 20px;
        background-color: #0b1f4d;
        color: white;
        border: 1px solid #0b1f4d;
        box-shadow: 0 8px 22px rgba(11, 31, 77, 0.22);
        margin-bottom: 20px;
    }

    .score-number {
        font-size: 62px;
        font-weight: 900;
        margin-bottom: 0px;
        color: white;
        line-height: 1.05;
    }

    .recommendation {
        font-size: 28px;
        font-weight: 800;
        margin-top: 6px;
        color: #8ab4ff;
    }

    .small-label {
        color: #cbd5e1;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 4px;
    }

    .card-label {
        color: #374151;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 4px;
        font-weight: 700;
    }

    .card-value {
        color: #0b1f4d;
        font-size: 30px;
        font-weight: 850;
        margin-bottom: 8px;
    }

    .muted-text {
        color: #4b5563;
        font-size: 15px;
        line-height: 1.5;
    }

    /* Section headers */
    h2, h3 {
        color: #0b1f4d;
    }

    /* Streamlit metric cards */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #dbe3f0;
        padding: 16px;
        border-radius: 16px;
        box-shadow: 0 3px 10px rgba(11, 31, 77, 0.06);
    }

    div[data-testid="stMetricLabel"] {
        color: #374151;
    }

    div[data-testid="stMetricValue"] {
        color: #0b1f4d;
        font-weight: 800;
    }

    /* Upload box */
    section[data-testid="stFileUploader"] {
        background-color: #f8fbff;
        border: 1px dashed #155eef;
        border-radius: 16px;
        padding: 16px;
    }

    /* Expander */
    details {
        border: 1px solid #dbe3f0;
        border-radius: 14px;
        background-color: #ffffff;
    }

    /* Horizontal spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <div class="hero-card">
        <h1>Kynthera Funds MVP</h1>
        <p>Cash-flow intelligence for SME lending. Turning transaction data into explainable credit decisions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Upload section
# -----------------------------
st.markdown("## Upload SME transaction data")

st.write(
    "Upload a CSV file with transaction data. In the full product, this input would come from "
    "PSD2 open banking APIs. For the MVP, a CSV upload simulates the same transaction-data input."
)

uploaded_file = st.file_uploader("Upload transaction CSV", type=["csv"])

if uploaded_file is None:
    st.info("Use the sample file: `data/sample_transactions.csv`.")
    st.stop()


# -----------------------------
# Load and process data
# -----------------------------
try:
    df = load_transactions(uploaded_file)
except Exception as e:
    st.error(f"Could not process file: {e}")
    st.stop()

metrics = calculate_cashflow_metrics(df)
result = calculate_credit_score(metrics)


# -----------------------------
# Recommendation logic
# -----------------------------
score = result["score"]
recommendation = result["recommendation"]

if recommendation == "Approve":
    recommendation_text = "Approve"
    recommendation_explanation = (
        "The SME shows sufficient cash-flow strength for a positive lending recommendation."
    )
elif recommendation == "Manual review":
    recommendation_text = "Manual Review"
    recommendation_explanation = (
        "The SME has mixed signals. A credit officer should review the case before approval."
    )
else:
    recommendation_text = "Reject"
    recommendation_explanation = (
        "The SME shows elevated cash-flow risk based on the available transaction data."
    )


# -----------------------------
# Risk report
# -----------------------------
st.markdown("## Kynthera Risk Report")

left, right = st.columns([1.2, 2])

with left:
    st.markdown(
        f"""
        <div class="score-card">
            <div class="small-label">Credit confidence score</div>
            <div class="score-number">{score}/100</div>
            <div class="recommendation">{recommendation_text}</div>
            <p>{recommendation_explanation}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        f"""
        <div class="section-card">
            <div class="card-label">Suggested maximum loan</div>
            <div class="card-value">€{result['suggested_max_loan']:,.0f}</div>
            <p class="muted-text">
                This loan estimate is based on the SME's average monthly revenue, cash-flow strength,
                and risk score. It is intended as a decision-support output, not as an automatic final credit decision.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# Cash-flow metrics
# -----------------------------
st.markdown("## Key Cash-flow Signals")

m1, m2, m3, m4 = st.columns(4)

m1.metric("Average monthly revenue", f"€{metrics['avg_monthly_revenue']:,.0f}")
m2.metric("Average monthly outflows", f"€{metrics['avg_monthly_outflows']:,.0f}")
m3.metric("Average balance", f"€{metrics['avg_balance']:,.0f}")
m4.metric("Negative balance days", metrics["negative_balance_days"])

m5, m6, m7, m8 = st.columns(4)

m5.metric("Revenue stability", f"{metrics['revenue_stability']:.2f}")
m6.metric("Liquidity buffer", f"{metrics['liquidity_buffer_months']:.2f} months")
m7.metric("Volatility risk", f"{metrics['cashflow_volatility']:.2f}")
m8.metric("Growth trend", f"{metrics['growth_trend'] * 100:.1f}%")


# -----------------------------
# Score drivers
# -----------------------------
st.markdown("## Explainable Score Drivers")

positive_drivers = [d for d in result["drivers"] if d[1] == "positive"]
neutral_drivers = [d for d in result["drivers"] if d[1] == "neutral"]
negative_drivers = [d for d in result["drivers"] if d[1] == "negative"]

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### Strengths")
    if positive_drivers:
        for name, status, explanation in positive_drivers:
            st.write(f"**{name}:** {explanation}")
    else:
        st.write("No major positive drivers identified.")

with c2:
    st.markdown("### Watchlist")
    if neutral_drivers:
        for name, status, explanation in neutral_drivers:
            st.write(f"**{name}:** {explanation}")
    else:
        st.write("No neutral drivers identified.")

with c3:
    st.markdown("### Risks")
    if negative_drivers:
        for name, status, explanation in negative_drivers:
            st.write(f"**{name}:** {explanation}")
    else:
        st.write("No major risk drivers identified.")


# -----------------------------
# Monthly chart
# -----------------------------
st.markdown("## Monthly Cash-flow Overview")

monthly_chart = metrics["monthly"].set_index("month")[["inflows", "outflows", "net_cashflow"]]
st.line_chart(monthly_chart)


# -----------------------------
# Transaction preview
# -----------------------------
with st.expander("View transaction data"):
    st.dataframe(df)