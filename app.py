# Import Streamlit, which is used to build the web app interface
import streamlit as st

# Import pandas, which is used to work with tabular data
import pandas as pd

# Import functions that load and process the transaction data
from src.data_processing import load_transactions, calculate_cashflow_metrics

# Import the function that calculates the credit score and recommendation
from src.scoring import calculate_credit_score


# -----------------------------
# Page configuration
# -----------------------------

# Set the browser tab title and use the full page width
st.set_page_config(
    page_title="Kynthera Funds MVP",
    layout="wide"
)


# -----------------------------
# Styling
# -----------------------------

# Inject custom CSS to control the colours, cards, spacing, and dashboard layout
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

    /* Custom signal cards */
    .signal-card {
        padding: 24px;
        border-radius: 18px;
        background-color: #ffffff;
        border: 1px solid #dbe3f0;
        box-shadow: 0 4px 14px rgba(11, 31, 77, 0.08);
        margin-bottom: 18px;
        min-height: 125px;
    }

    .signal-label {
        color: #111827 !important;
        font-size: 15px;
        font-weight: 750;
        margin-bottom: 16px;
    }

    .signal-value {
        color: #0b1f4d !important;
        font-size: 34px;
        font-weight: 900;
        line-height: 1.1;
    }

    /* Section headers */
    h1, h2, h3 {
        color: #0b1f4d;
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

    /* Methodology table */
    table {
        border-collapse: collapse;
        width: 100%;
    }

    thead tr th {
        background-color: #0b1f4d !important;
        color: white !important;
        font-weight: 700 !important;
    }

    tbody tr td {
        color: #0b0f19 !important;
    }

    /* Page spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Helper for custom metric cards
# -----------------------------

# Display one cash-flow metric as a reusable styled card
def signal_card(label, value):
    st.markdown(
        f"""
        <div class="signal-card">
            <div class="signal-label">{label}</div>
            <div class="signal-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# Header
# -----------------------------

# Display the main app title and description
st.markdown(
    """
    <div class="hero-card">
        <h1>Kynthera Funds MVP</h1>
        <p>
            Cash-flow intelligence for SME lending.
            Turning transaction data into explainable credit decisions.
        </p>
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

# Allow the user to upload a CSV file containing transaction data
uploaded_file = st.file_uploader(
    "Upload transaction CSV",
    type=["csv"]
)

# Stop the app until a file has been uploaded
if uploaded_file is None:
    st.info("Use the sample file: `data/sample_transactions.csv`.")
    st.stop()


# -----------------------------
# Load and process data
# -----------------------------

# Try to load and validate the uploaded transaction file
try:
    df = load_transactions(uploaded_file)

# Show an error and stop the app if the file cannot be processed
except Exception as e:
    st.error(f"Could not process file: {e}")
    st.stop()

# Calculate the cash-flow metrics used by the scoring model
metrics = calculate_cashflow_metrics(df)

# Generate the credit score, recommendation, loan estimate, and score drivers
result = calculate_credit_score(metrics)


# -----------------------------
# Recommendation logic
# -----------------------------

# Extract the main scoring results
score = result["score"]
recommendation = result["recommendation"]

# Convert the recommendation into clear user-facing text
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

# Display the main credit risk output
st.markdown("## Kynthera Risk Report")

# Place the credit score and loan estimate next to each other
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
            <div class="card-value">
                €{result['suggested_max_loan']:,.0f}
            </div>
            <p class="muted-text">
                This loan estimate is based on the SME's average monthly revenue,
                cash-flow strength, and risk score. It is intended as a
                decision-support output, not as an automatic final credit decision.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# Cash-flow metrics
# -----------------------------

# Display the core cash-flow signals used in the lending assessment
st.markdown("## Key Cash-flow Signals")

m1, m2, m3, m4 = st.columns(4)

with m1:
    signal_card(
        "Average monthly revenue",
        f"€{metrics['avg_monthly_revenue']:,.0f}"
    )

with m2:
    signal_card(
        "Average monthly outflows",
        f"€{metrics['avg_monthly_outflows']:,.0f}"
    )

with m3:
    signal_card(
        "Average balance",
        f"€{metrics['avg_balance']:,.0f}"
    )

with m4:
    signal_card(
        "Negative balance days",
        metrics["negative_balance_days"]
    )

m5, m6, m7, m8 = st.columns(4)

with m5:
    signal_card(
        "Revenue stability",
        f"{metrics['revenue_stability']:.2f}"
    )

with m6:
    signal_card(
        "Liquidity buffer",
        f"{metrics['liquidity_buffer_months']:.2f} months"
    )

with m7:
    signal_card(
        "Volatility risk",
        f"{metrics['cashflow_volatility']:.2f}"
    )

with m8:
    signal_card(
        "Growth trend",
        f"{metrics['growth_trend'] * 100:.1f}%"
    )


# -----------------------------
# Score drivers
# -----------------------------

st.markdown("## Explainable Score Drivers")

# Group the score drivers into strengths, watchlist items, and risks
positive_drivers = [
    driver for driver in result["drivers"]
    if driver[1] == "positive"
]

neutral_drivers = [
    driver for driver in result["drivers"]
    if driver[1] == "neutral"
]

negative_drivers = [
    driver for driver in result["drivers"]
    if driver[1] == "negative"
]

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

# Select the monthly metrics to display in the line chart
monthly_chart = (
    metrics["monthly"]
    .set_index("month")[["inflows", "outflows", "net_cashflow"]]
)

st.line_chart(monthly_chart)


# -----------------------------
# Transaction preview
# -----------------------------

# Allow the user to inspect the processed transaction data
with st.expander("View transaction data"):
    st.dataframe(
        df,
        use_container_width=True
    )


# -----------------------------
# Score methodology explanation
# -----------------------------

st.markdown("## How the Score Is Calculated")

st.write(
    "The Kynthera score is a transparent rule-based score from 0 to 100. "
    "The MVP starts from a neutral base score of 50 points and then adjusts the score "
    "based on five cash-flow signals."
)

# Define the scoring rules displayed in the methodology table
methodology_data = [
    {
        "Cash-flow signal": "Revenue stability",
        "Condition": "≥ 0.75",
        "Score effect": "+15",
        "Interpretation": "Monthly revenue is relatively stable",
    },
    {
        "Cash-flow signal": "Revenue stability",
        "Condition": "0.50 to 0.74",
        "Score effect": "+8",
        "Interpretation": "Monthly revenue is moderately stable",
    },
    {
        "Cash-flow signal": "Revenue stability",
        "Condition": "< 0.50",
        "Score effect": "-8",
        "Interpretation": "Monthly revenue is unstable",
    },
    {
        "Cash-flow signal": "Liquidity buffer",
        "Condition": "≥ 1.50 months",
        "Score effect": "+15",
        "Interpretation": "Average balance covers more than 1.5 months of outflows",
    },
    {
        "Cash-flow signal": "Liquidity buffer",
        "Condition": "0.75 to 1.49 months",
        "Score effect": "+7",
        "Interpretation": "Liquidity buffer is acceptable but not strong",
    },
    {
        "Cash-flow signal": "Liquidity buffer",
        "Condition": "< 0.75 months",
        "Score effect": "-10",
        "Interpretation": "Liquidity buffer is weak",
    },
    {
        "Cash-flow signal": "Negative balance days",
        "Condition": "0% of observed days",
        "Score effect": "+10",
        "Interpretation": "No negative balance days observed",
    },
    {
        "Cash-flow signal": "Negative balance days",
        "Condition": "≤ 5% of observed days",
        "Score effect": "+3",
        "Interpretation": "Only a few negative balance days observed",
    },
    {
        "Cash-flow signal": "Negative balance days",
        "Condition": "> 5% of observed days",
        "Score effect": "-12",
        "Interpretation": "Frequent negative balance days increase liquidity risk",
    },
    {
        "Cash-flow signal": "Cash-flow volatility",
        "Condition": "≤ 0.80",
        "Score effect": "+10",
        "Interpretation": "Net cash flow is relatively predictable",
    },
    {
        "Cash-flow signal": "Cash-flow volatility",
        "Condition": "0.81 to 1.30",
        "Score effect": "+2",
        "Interpretation": "Net cash flow shows moderate volatility",
    },
    {
        "Cash-flow signal": "Cash-flow volatility",
        "Condition": "> 1.30",
        "Score effect": "-10",
        "Interpretation": "Net cash flow is highly volatile",
    },
    {
        "Cash-flow signal": "Growth trend",
        "Condition": "≥ 10%",
        "Score effect": "+10",
        "Interpretation": "Revenue increased over the observed period",
    },
    {
        "Cash-flow signal": "Growth trend",
        "Condition": "-10% to 9.9%",
        "Score effect": "+3",
        "Interpretation": "Revenue trend is broadly stable",
    },
    {
        "Cash-flow signal": "Growth trend",
        "Condition": "< -10%",
        "Score effect": "-8",
        "Interpretation": "Revenue declined over the observed period",
    },
]

# Convert the scoring rules into a table
methodology_df = pd.DataFrame(methodology_data)
st.table(methodology_df)

# Explain the limitations of the current MVP scoring model
st.caption(
    "The final score is capped between 0 and 100. In this MVP, the scoring rules are "
    "intentionally simple and explainable. In a production version, these thresholds "
    "would be validated and calibrated using real repayment and default outcome data."
)
