# pages/1_Overview.py

import streamlit as st
import pandas as pd
import plotly.express as px
from db_connection import get_connection

st.set_page_config(layout="wide")
st.title("Dataset Overview & EDA")
st.markdown("This section explores the synthetic auto insurance dataset using SQL-driven exploratory analysis. "
            "Key metrics include claim rates by age, income, credit bands, and regional segments.")
st.markdown(
    "This analysis is based on the [_Car Insurance Claim_](https://www.kaggle.com/datasets/sagnik1511/car-insurance-data/data) dataset from Kaggle, "
    "which was cleaned, normalized, and split into four SQL tables shown below."
)

# ----------------------------
# Cached query runner
# ----------------------------
@st.cache_data
def run_query(label, sql):
    conn = get_connection()
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

# ----------------------------
# Top Metrics
# ----------------------------
summary_sql = """
    SELECT 
        COUNT(*) AS total_customers,
        SUM(outcome) AS total_claims,
        ROUND(SUM(outcome) / COUNT(*), 2) AS claim_rate
    FROM claims;
"""
summary = run_query("summary", summary_sql)
st.subheader("Portfolio Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", f"{summary['total_customers'][0]:,}")
col2.metric("Total Claims", f"{summary['total_claims'][0]:,}")
col3.metric("Claim Rate", f"{int(summary['claim_rate'][0]*100)}%")

# Show previews of the core SQL tables
table_queries = {
    "Customers": "SELECT * FROM customers LIMIT 5;",
    "Vehicles": "SELECT * FROM vehicles LIMIT 5;",
    "Driving History": "SELECT * FROM driving_history LIMIT 5;",
    "Claims": "SELECT * FROM claims LIMIT 5;"
}

cols = st.columns(2)
for i, (label, query) in enumerate(table_queries.items()):
    with cols[i % 2]:
        st.markdown(f"#### `{label}` Table")
        st.dataframe(run_query(label, query), use_container_width=True)

st.divider()

# ----------------------------
# Layout Utility
# ----------------------------
def render_section(title, sql, df, chart=None, layout="visual", note=None):
    st.subheader(title)

    if layout == "left_chart":
        col1, col2 = st.columns((1, 1))
        col2.plotly_chart(chart, use_container_width=True)
        with col1:
            st.dataframe(df, use_container_width=True)
            with st.expander("View underlying SQL"):
                st.code(sql.strip(), language="sql")
        
    elif layout == "right_chart":
        col1, col2 = st.columns((1, 1))        
        with col2:
            st.dataframe(df, use_container_width=True)
            with st.expander("View underlying SQL"):
                st.code(sql.strip(), language="sql")
        col1.plotly_chart(chart, use_container_width=True)

    elif layout == "visual":
        st.plotly_chart(chart, use_container_width=True)
        if note:
            st.caption(note)
        with st.expander("View underlying SQL"):
            st.code(sql.strip(), language="sql")

    if layout != "visual" and note:
        st.caption(note)

    st.divider()


# ----------------------------
# 1. Claim Rate by Postal Code
# ----------------------------
sql1 = """
SELECT c.postal_code,
       COUNT(*) AS total_customers,
       SUM(cl.outcome) AS total_claims,
       ROUND(SUM(cl.outcome) / COUNT(*), 2) AS claim_rate
FROM customers c
JOIN claims cl ON c.id = cl.id
GROUP BY c.postal_code
ORDER BY claim_rate DESC;
"""
df1 = run_query("postal", sql1)
df1["postal_code"] = df1["postal_code"].astype(str)
fig1 = px.bar(df1, x="postal_code", y="claim_rate", category_orders={"postal_code": df1["postal_code"].tolist()})
fig1.update_xaxes(type='category')
render_section("1. Claim Rate by Postal Code", sql1, df1, chart=fig1, layout="left_chart",
               note="Certain postal codes show significantly higher claim rates, suggesting potential geographic risk clusters or fraud hotspots.")

# ----------------------------
# 2. Risk by Income Bracket
# ----------------------------
sql2 = """
SELECT c.income,
       ROUND(AVG(rs.risk_score), 2) AS avg_risk_score,
       ROUND(SUM(cl.outcome) / COUNT(*), 2) AS claim_rate,
       COUNT(*) AS total_customers
FROM customers c
JOIN risk_scores rs ON c.id = rs.id
JOIN claims cl ON c.id = cl.id
GROUP BY c.income
ORDER BY avg_risk_score DESC;
"""
df2 = run_query("income", sql2)
fig2 = px.bar(df2, x="income", y="avg_risk_score", color="claim_rate", barmode="group")
render_section("2. Risk by Income Bracket", sql2, df2, chart=fig2, layout="right_chart",
               note="Higher risk scores and claim rates are concentrated in lower income brackets, indicating socioeconomic correlation with insurance risk.")

# ----------------------------
# 3. Risk by Gender
# ----------------------------
sql3 = """
SELECT c.gender,
       ROUND(AVG(rs.risk_score), 2) AS avg_risk_score,
       ROUND(SUM(cl.outcome) / COUNT(*), 2) AS claim_rate,
       COUNT(*) AS total_customers
FROM customers c
JOIN risk_scores rs ON c.id = rs.id
JOIN claims cl ON c.id = cl.id
GROUP BY c.gender
ORDER BY avg_risk_score DESC;
"""
df3 = run_query("gender", sql3)
df3_melted = df3.melt(
    id_vars="gender",
    value_vars=["avg_risk_score", "claim_rate"],
    var_name="metric",
    value_name="value"
)
fig3 = px.bar(
    df3_melted,
    x="gender", y="value", color="metric", barmode="group", text="value",
    labels={"value": "Metric Value", "gender": "Gender", "metric": "Metric"}
)
fig3.update_traces(textposition="outside")
fig3.update_layout(showlegend=True)
fig3.update_layout(height=500)
render_section("3. Risk & Claim Rate by Gender", sql3, df3, chart=fig3, layout="left_chart",
               note="Male customers show slightly higher average risk scores and claim rates compared to females, suggesting mild gender-based risk variation.")

# ----------------------------
# 4. Mileage by Vehicle Type
# ----------------------------
sql4 = """
SELECT vehicle_type,
       ROUND(AVG(annual_mileage), 0) AS avg_annual_mileage,
       COUNT(*) AS total_vehicles
FROM vehicles
GROUP BY vehicle_type
ORDER BY avg_annual_mileage DESC;
"""
df4 = run_query("vehicle_type", sql4)
fig4 = px.bar(
    df4.melt(id_vars="vehicle_type", value_vars=["avg_annual_mileage", "total_vehicles"]),
    x="vehicle_type",
    y="value",
    color="variable",
    barmode="group",
    text="value"
)
fig4.update_traces(textposition="outside")
fig4.update_layout(height=500)
render_section("4. Mileage by Vehicle Type", sql4, df4, chart=fig4, layout="right_chart",
               note="Sedan car drivers tend to log higher mileage annually than sports drivers, which may increase exposure and claim likelihood.")

# ----------------------------
# 5. Claim Rate by Age
# ----------------------------
sql5 = """
SELECT age,
       COUNT(*) AS total_customers,
       SUM(cl.outcome) AS total_claims,
       ROUND(SUM(cl.outcome) / COUNT(*), 2) AS claim_rate
FROM customers c
JOIN claims cl ON c.id = cl.id
GROUP BY age
ORDER BY claim_rate DESC;
"""
df5 = run_query("age", sql5)
fig5 = px.line(df5.sort_values("age"), x="age", y="claim_rate")
render_section("5. Claim Rate by Age", sql5, df5, chart=fig5, layout="visual",
               note="Younger drivers (under 25) exhibit the highest claim rates, likely due to inexperience.")

# ----------------------------
# 6. Risk Score vs Claim Rate
# ----------------------------
sql6 = """
SELECT risk_score,
       COUNT(*) AS total_customers,
       SUM(outcome) AS total_claims,
       ROUND(SUM(outcome) / COUNT(*), 2) AS claim_rate
FROM risk_scores rs
JOIN claims cl ON rs.id = cl.id
GROUP BY risk_score
ORDER BY risk_score DESC;
"""
df6 = run_query("risk_score_summary", sql6)
fig6 = px.area(df6.sort_values("risk_score"), x="risk_score", y="claim_rate")
render_section("6. Risk Score vs. Claim Rate", sql6, df6, chart=fig6, layout="visual",
               note="Risk scoring is effective — as risk scores increase, claim rates consistently rise, validating the predictive value of the scoring logic.")

# ----------------------------
# 7. Claim Rate by Age + Income
# ----------------------------
sql7 = """
SELECT age, income, 
       COUNT(*) AS total_customers,
       SUM(cl.outcome) AS total_claims,
       ROUND(SUM(cl.outcome) / COUNT(*), 2) AS claim_rate
FROM customers c
JOIN claims cl ON c.id = cl.id
GROUP BY age, income
ORDER BY age, income;
"""
df7 = run_query("age_income", sql7)
fig7 = px.density_heatmap(
    df7, x="age", y="income", z="claim_rate",
    nbinsx=20, color_continuous_scale="Blues",
    category_orders={
        "income": ["upper class", "middle class", "working class", "poverty"]
    }
)
fig7.update_coloraxes(colorbar_title="Average Claim Rate")
render_section("7. Claim Rate by Age and Income", sql7, df7, chart=fig7, layout="visual",
               note="Claim patterns vary by both age and income — certain age-income intersections show concentrated risk, as revealed by this heatmap.")

# ----------------------------
# 8. Driving Experience & Claims
# ----------------------------
sql8 = """
SELECT driving_experience,
       COUNT(*) AS total_customers,
       SUM(cl.outcome) AS total_claims,
       ROUND(SUM(cl.outcome) / COUNT(*), 2) AS claim_rate
FROM driving_history d
JOIN claims cl ON d.id = cl.id
GROUP BY driving_experience
ORDER BY claim_rate DESC;
"""
df8 = run_query("experience", sql8)
fig8 = px.bar(df8.sort_values("driving_experience"), x="driving_experience", y="claim_rate")
render_section("8. Claim Rate by Driving Experience", sql8, df8, chart=fig8, layout="left_chart",
               note="Less experienced drivers (under 10 years) have much higher claim rates, affirming that experience plays a major role in reducing risk.")

# ----------------------------
# 9. Claims by Vehicle Year
# ----------------------------
sql9 = """
SELECT vehicle_year,
       COUNT(*) AS total_vehicles,
       ROUND(AVG(annual_mileage), 0) AS avg_annual_mileage,
       ROUND(SUM(cl.outcome) / COUNT(*), 2) AS claim_rate
FROM vehicles v
JOIN claims cl ON v.id = cl.id
GROUP BY vehicle_year
ORDER BY claim_rate DESC;
"""
df9 = run_query("vehicle_year", sql9)
fig9 = px.pie(df9, names="vehicle_year", values="claim_rate")
render_section("9. Claim Rate by Vehicle Year", sql9, df9, chart=fig9, layout="visual",
               note="Claim rates are higher for older vehicles, possibly due to wear, lower safety standards, or other risk indicators.")

# ----------------------------
# 10. Risk Score Distribution
# ----------------------------
sql10 = """
SELECT risk_score,
       COUNT(*) AS num_customers
FROM risk_scores
GROUP BY risk_score
ORDER BY risk_score DESC;
"""
df10 = run_query("risk_score_dist", sql10)
fig10 = px.histogram(df10, x="risk_score", y="num_customers", nbins=10)
fig10.update_xaxes(dtick=1)
render_section("10. Risk Score Distribution", sql10, df10, chart=fig10, layout="visual",
               note="Risk score distribution shows a healthy spread across the portfolio, though most customers cluster at scores between 0–2.")

# ----------------------------
# 11. Risk by Credit Score Band
# ----------------------------
sql11 = """
SELECT
   CASE
      WHEN credit_score < 0.4 THEN 'Very Low'
      WHEN credit_score < 0.6 THEN 'Low'
      WHEN credit_score < 0.8 THEN 'Medium'
      ELSE 'High'
   END AS credit_band,
   ROUND(AVG(rs.risk_score), 2) AS avg_risk_score,
   ROUND(AVG(cl.outcome), 2) AS claim_rate,
   COUNT(*) AS total_customers
FROM customers c
JOIN risk_scores rs ON c.id = rs.id
JOIN claims cl ON c.id = cl.id
GROUP BY credit_band
ORDER BY claim_rate DESC;
"""
df11 = run_query("credit_band", sql11)
fig11 = px.bar(df11, x="credit_band", y="avg_risk_score", color="claim_rate")
render_section("11. Risk by Credit Score Band", sql11, df11, chart=fig11, layout="right_chart",
               note="Stronger credit scores correlate with lower average risk and claim rates — very low credit bands carry significantly higher risk.")
