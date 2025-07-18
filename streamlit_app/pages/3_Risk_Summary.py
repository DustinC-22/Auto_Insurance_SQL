# pages/5_Dashboard_summary.py

import streamlit as st
import pandas as pd
import plotly.express as px
from db_connection import get_connection

st.title("Risk Summary")
st.markdown("This dashboard summarizes portfolio-wide performance using the risk scoring logic. "
            "It highlights claim rates by customer segment, risk distribution, and performance by score tier.")

# -----------------------------
# SQL Data Loader
# -----------------------------
@st.cache_data
def load_dashboard_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    queries = {
        "Portfolio KPIs": """
            SELECT COUNT(*) AS total_customers,
                   SUM(outcome) AS total_claims,
                   ROUND(SUM(outcome) / COUNT(*), 2) AS overall_claim_rate
            FROM claims;
        """,
        "High-Risk Snapshot": """
            SELECT COUNT(*) AS high_risk_customers,
                   SUM(outcome) AS total_claims,
                   ROUND(SUM(outcome) / COUNT(*), 2) AS claim_rate
            FROM risk_scores rs
            JOIN claims cl ON rs.id = cl.id
            WHERE risk_score >= 3;
        """,
        "Claim Rate by Risk Tier": """
            SELECT
               CASE
                  WHEN risk_score >= 3 THEN 'High Risk'
                  WHEN risk_score = 2 THEN 'Medium Risk'
                  ELSE 'Low Risk'
               END AS risk_category,
               COUNT(*) AS num_customers,
               SUM(outcome) AS total_claims,
               ROUND(SUM(outcome) / COUNT(*), 2) AS claim_rate
            FROM risk_scores rs
            JOIN claims cl ON rs.id = cl.id
            GROUP BY risk_category
            ORDER BY claim_rate DESC;
        """,
        "Risk Score Distribution": """
            SELECT risk_score,
                   COUNT(*) AS num_customers,
                   ROUND(100 * COUNT(*) / (SELECT COUNT(*) FROM risk_scores), 1) AS pct_of_portfolio
            FROM risk_scores
            GROUP BY risk_score
            ORDER BY risk_score DESC;
        """,
        "Extremes Comparison": """
            SELECT 'High Risk (3+)' AS risk_group,
                   COUNT(*) AS num_customers,
                   SUM(outcome) AS total_claims,
                   ROUND(SUM(outcome) / COUNT(*), 2) AS claim_rate
            FROM risk_scores rs
            JOIN claims cl ON rs.id = cl.id
            WHERE risk_score >= 3

            UNION ALL

            SELECT 'Low Risk (0-1)' AS risk_group,
                   COUNT(*) AS num_customers,
                   SUM(outcome) AS total_claims,
                   ROUND(SUM(outcome) / COUNT(*), 2) AS claim_rate
            FROM risk_scores rs
            JOIN claims cl ON rs.id = cl.id
            WHERE risk_score <= 1;
        """,
        "Claim Load by Risk Score": """
            SELECT risk_score,
                   SUM(outcome) AS total_claims,
                   COUNT(*) AS total_customers,
                   ROUND(SUM(outcome) / COUNT(*), 2) AS claim_rate
            FROM risk_scores rs
            JOIN claims cl ON rs.id = cl.id
            GROUP BY risk_score
            ORDER BY total_claims DESC;
        """
    }

    data = {}
    for name, sql in queries.items():
        cursor.execute(sql)
        df = pd.DataFrame(cursor.fetchall())
        df.attrs["query"] = sql
        data[name] = df

    cursor.close()
    conn.close()
    return data


# -----------------------------
# Load Data
# -----------------------------
data = load_dashboard_data()


# -----------------------------
# Portfolio KPIs
# -----------------------------
st.subheader("Portfolio KPIs")

kpis = data["Portfolio KPIs"].iloc[0]
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", f"{kpis['total_customers']:,}")
col2.metric("Total Claims", f"{kpis['total_claims']:,}")
col3.metric("Overall Claim Rate", f"{int(kpis['overall_claim_rate'] * 100)}%")

# -----------------------------
# High-Risk Snapshot
# -----------------------------
st.subheader("High-Risk Segment")
high_risk = data["High-Risk Snapshot"].iloc[0]
st.markdown(f"""
High-risk customers are defined as those with a risk score ≥ 3.

- Number of high-risk customers: {high_risk['high_risk_customers']:,}
- Claims filed by high-risk customers: {high_risk['total_claims']:,}
- Claim rate in this segment: {int(high_risk['claim_rate'] * 100)}%
""")

with st.expander("View underlying SQL"):
    st.code(data["High-Risk Snapshot"].attrs["query"], language="sql")

col1, col2 = st.columns([1,1])
with col1:
    # Claim Rate by Risk Category
    st.subheader("Claim Rate by Risk Tier")

    tier_df = data["Claim Rate by Risk Tier"]
    fig = px.bar(tier_df, x="risk_category", y="claim_rate",
                 text="claim_rate", labels={"risk_category": "Risk Tier", "claim_rate": "Claim Rate"},
                 color="risk_category")
    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("View underlying SQL"):
        st.code(tier_df.attrs["query"], language="sql")

with col2:
    # Risk Score Distribution
    st.subheader("Risk Score Distribution")
    
    dist_df = data["Risk Score Distribution"]
    fig2 = px.pie(dist_df, names="risk_score", values="pct_of_portfolio")
    fig2.update_layout(legend=dict(traceorder="reversed"))
    
    st.plotly_chart(fig2, use_container_width=True)
    
    with st.expander("View underlying SQL"):
        st.code(dist_df.attrs["query"], language="sql")

# -----------------------------
# Total Claim Load by Risk Score
# -----------------------------
st.subheader("Total Claims by Risk Score")

load_df = data["Claim Load by Risk Score"]
fig3 = px.bar(load_df, x="total_claims", y="risk_score", orientation="h",
              labels={"total_claims": "Total Claims", "risk_score": "Risk Score"},
              color="risk_score", text="total_claims")
fig3.update_coloraxes(showscale=False)

st.plotly_chart(fig3, use_container_width=True)

with st.expander("View underlying SQL"):
    st.code(load_df.attrs["query"], language="sql")

# -----------------------------
# Extremes Comparison
# -----------------------------
st.subheader("Comparison: High vs Low Risk Groups")

comp_df = data["Extremes Comparison"]
st.dataframe(comp_df, use_container_width=True)

with st.expander("View underlying SQL"):
    st.code(comp_df.attrs["query"], language="sql")
