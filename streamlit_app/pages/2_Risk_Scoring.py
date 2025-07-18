# pages/2_Risk_scoring.py

import streamlit as st
import pandas as pd
import plotly.express as px
from db_connection import get_connection

st.title("Risk Scoring")

st.markdown("""
The risk scoring system assigns each customer a score between 0 and 5, based on five behavioural and demographic factors.
Each factor is encoded as a binary flag (0 or 1), and the total score is simply the sum of all flags.

Risk Flags:
- Speeding Risk: More than 5 speeding violations.
- DUI Risk: At least one recorded DUI.
- Low Credit Score: Credit score below 0.5.
- Vehicle Risk: Vehicle is from before 2015 and has mileage over 15,000 km/year.
- Young Driver Risk: Drivers aged 16–25 with <10 years of experience.

These flags are defined and combined using SQL `CASE` logic and stored in a view called `risk_scores`.
""")

# ---------------------------
# Query Loader (Cached)
# ---------------------------
@st.cache_data
def load_risk_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    queries = {
        "Component Flags": """
            SELECT rs.id,
                   rs.speeding_risk,
                   rs.dui_risk,
                   rs.low_credit_risk,
                   rs.vehicle_risk,
                   rs.young_driver_risk,
                   rs.risk_score
            FROM risk_scores rs
            LIMIT 50;
        """,
        "Score vs. Claim Rate": """
            SELECT risk_score,
                   COUNT(*) AS total_customers,
                   SUM(outcome) AS total_claims,
                   ROUND(SUM(outcome) / COUNT(*), 2) AS claim_rate
            FROM risk_scores rs
            JOIN claims c ON rs.id = c.id
            GROUP BY risk_score
            ORDER BY risk_score;
        """,
        "High-Risk Customers": """
            SELECT rs.id, rs.risk_score, c.outcome
            FROM risk_scores rs
            JOIN claims c ON rs.id = c.id
            ORDER BY rs.risk_score DESC, c.outcome DESC
            LIMIT 20;
        """,
        "Risk Flag Distribution": """
            SELECT 
                SUM(speeding_risk) AS speeding,
                SUM(dui_risk) AS dui,
                SUM(low_credit_risk) AS credit,
                SUM(vehicle_risk) AS vehicle,
                SUM(young_driver_risk) AS young
            FROM risk_scores;
        """
    }

    results = {}
    for label, sql in queries.items():
        cursor.execute(sql)
        results[label] = pd.DataFrame(cursor.fetchall())
        results[label].attrs["query"] = sql

    cursor.close()
    conn.close()
    return results


# ---------------------------
# Load all data
# ---------------------------
data = load_risk_data()
flags_df = data["Component Flags"]
score_df = data["Score vs. Claim Rate"]
highrisk_df = data["High-Risk Customers"]
flag_counts = data["Risk Flag Distribution"]

# ---------------------------
# Component Pie Charts
# ---------------------------
st.subheader("Distribution of Risk Flags")

st.markdown("Each pie chart shows the proportion of customers flagged for each risk factor:")

col_titles = ["Speeding", "DUI", "Low Credit", "Vehicle", "Young Driver"]
flag_names = ["speeding", "dui", "credit", "vehicle", "young"]
cols = st.columns(5)

total_customers = 8149  # Optional: change dynamically if needed

for i, col in enumerate(cols):
    with col:
        flag = flag_names[i]
        title = col_titles[i]
        count = flag_counts[flag][0]
        chart = px.pie(
            names=["Flagged", "Not Flagged"],
            values=[count, total_customers - count],
            title=title, color_discrete_sequence=px.colors.sequential.RdBu
        )
        col.plotly_chart(chart, use_container_width=True)

# ---------------------------
# Component Flag Table
# ---------------------------
st.subheader("Risk Score Component Flags")
st.markdown("Each row shows a customer's individual binary flags and total risk score (sum of flags).")

st.dataframe(flags_df, use_container_width=True)

with st.expander("View underlying SQL"):
    st.code(data["Component Flags"].attrs["query"], language="sql")


# ---------------------------
# Line Chart: Risk Score vs Claim Rate
# ---------------------------
st.subheader("Risk Score vs. Claim Rate")
st.markdown("Higher risk scores are associated with higher claim rates, validating the scoring logic.")

fig = px.line(score_df, x="risk_score", y="claim_rate", markers=True,
              labels={"claim_rate": "Claim Rate", "risk_score": "Risk Score"},
              color_discrete_sequence=px.colors.sequential.Bluered_r)

st.plotly_chart(fig, use_container_width=True)

with st.expander("View underlying SQL"):
    st.code(data["Score vs. Claim Rate"].attrs["query"], language="sql")

# ---------------------------
# High-Risk Customers Table
# ---------------------------
st.subheader("High-Risk Customers")
st.markdown("These customers have the highest risk scores and are more likely to have filed a claim.")

st.dataframe(highrisk_df, use_container_width=True)

with st.expander("View underlying SQL"):
    st.code(data["High-Risk Customers"].attrs["query"], language="sql")
