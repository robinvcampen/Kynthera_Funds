import streamlit as st
from src.data_processing import load_transactions, calculate_cashflow_metrics
from src.scoring import calculate_credit_score

st.set_page_config(page_title="Kynthera MVP", layout="wide")

st.title("Kynthera Funds MVP")
st.subheader("Cash-flow intelligence for SME lending")

st.write(
    "Upload SME transaction data to generate an explainable cash-flow based "
    "credit confidence score and lending recommendation."
)

uploaded_file = st.file_uploader("Upload a transaction CSV", type=["csv"])

if uploaded_file is None:
    st.info("Upload a CSV file, or use the sample file in data/sample_transactions.csv.")
    st.stop()

try:
    df = load_transactions(uploaded_file)
except Exception as e:
    st.error(f"Could not process file: {e}")
    st.stop()

metrics = calculate_cashflow_metrics(df)
result = calculate_credit_score(metrics)

st.header("Credit Recommendation")

col1, col2, col3 = st.columns(3)
col1.metric("Credit confidence score", f"{result['score']}/100")
col2.metric("Recommendation", result["recommendation"])
col3.metric("Suggested max loan", f"€{result['suggested_max_loan']:,.0f}")

st.header("Cash-flow Metrics")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Avg monthly revenue", f"€{metrics['avg_monthly_revenue']:,.0f}")
m2.metric("Avg monthly outflows", f"€{metrics['avg_monthly_outflows']:,.0f}")
m3.metric("Avg balance", f"€{metrics['avg_balance']:,.0f}")
m4.metric("Negative balance days", metrics["negative_balance_days"])

st.header("Score Drivers")

for name, status, explanation in result["drivers"]:
    st.write(f"**{name}** ({status}): {explanation}")

st.header("Monthly Cash-flow Overview")
monthly_chart = metrics["monthly"].set_index("month")[["inflows", "outflows", "net_cashflow"]]
st.line_chart(monthly_chart)

st.header("Transaction Preview")
st.dataframe(df.head(20))
