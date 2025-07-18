import streamlit as st
import pandas as pd
import plotly.express as px
from db_connection import get_connection

st.title("Dashboard")
st.markdown("""
This tool allows you to explore specific customer segments based on demographic and behavioural filters.
You can filter by risk score, age, income, credit score, and driving experience to examine claim behaviour, risk patterns, and segment composition.
""")

# ---------------------------
# Sidebar filters
# ---------------------------
st.sidebar.header("Segment Filters")

risk_range = st.sidebar.slider("Risk Score Range", 0, 5, (0, 5))
age_options = st.sidebar.multiselect("Age Group", ["16-25", "26-39", "40-64", "65+"], default=["16-25", "26-39", "40-64", "65+"])
income_options = st.sidebar.multiselect("Income Bracket", ["poverty", "working class", "middle class", "upper class"],
                                        default=["poverty", "working class", "middle class", "upper class"])
experience_options = st.sidebar.multiselect("Driving Experience", ["0-9y", "10-19y", "20-29y", "30y+"],
                                            default=["0-9y", "10-19y", "20-29y", "30y+"])
credit_range = st.sidebar.slider("Credit Score Range", 0.0, 1.0, (0.0, 1.0))

# ---------------------------
# Dynamic SQL Generator
# ---------------------------
def build_sql_from_filters():
    query = """
    SELECT rs.id, rs.risk_score, c.age, c.income, c.credit_score, d.driving_experience, cl.outcome
    FROM risk_scores rs
    JOIN customers c ON rs.id = c.id
    JOIN driving_history d ON rs.id = d.id
    JOIN claims cl ON rs.id = cl.id
    WHERE 1=1
    """

    if age_options:
        age_str = ",".join(f"'{a}'" for a in age_options)
        query += f"\nAND c.age IN ({age_str})"

    if income_options:
        inc_str = ",".join(f"'{i}'" for i in income_options)
        query += f"\nAND c.income IN ({inc_str})"

    if experience_options:
        exp_str = ",".join(f"'{e}'" for e in experience_options)
        query += f"\nAND d.driving_experience IN ({exp_str})"

    if risk_range != (0, 5):
        query += f"\nAND rs.risk_score BETWEEN {risk_range[0]} AND {risk_range[1]}"

    if credit_range != (0.0, 1.0):
        query += f"\nAND c.credit_score BETWEEN {credit_range[0]} AND {credit_range[1]}"

    query += "\nORDER BY rs.risk_score DESC, cl.outcome DESC;"
    return query

# ---------------------------
# Load filtered data
# ---------------------------
@st.cache_data
def load_segment(sql):
    conn = get_connection()
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

sql_query = build_sql_from_filters()
segment = load_segment(sql_query)

# ---------------------------
# Segment Summary Metrics
# ---------------------------
st.subheader("Segment Summary")
st.markdown(f"Filtered segment includes {len(segment):,} customers.")

col1, col2, col3 = st.columns(3)
col1.metric("Avg. Risk Score", f"{segment['risk_score'].mean():.2f}")
col2.metric("Claim Rate", f"{segment['outcome'].mean() * 100:.2f}%")
col3.metric("Avg. Credit Score", f"{segment['credit_score'].mean():.2f}")

# ---------------------------
# Segment Table
# ---------------------------
st.dataframe(segment, use_container_width=True)

with st.expander("View underlying SQL template"):
    st.code(sql_query.strip(), language="sql")

# ---------------------------
# Export Filtered Segment
# ---------------------------
csv = segment.to_csv(index=False).encode('utf-8')
st.download_button("📥 Export Segment as CSV", csv, "segment.csv", "text/csv")

# ---------------------------
# Segment Visuals
# ---------------------------
if len(segment) > 0:
    st.subheader("Segment Composition")
    col4, col5 = st.columns([1,1])

    with col4:
        # Age Distribution
        age_counts = segment["age"].value_counts().reset_index()
        age_counts.columns = ["age", "count"]
        age_order = ["16-25", "26-39", "40-64", "65+"]
        age_counts["age"] = pd.Categorical(age_counts["age"], categories=age_order, ordered=True)
        age_counts = age_counts.sort_values("age")

        dash_fig1 = px.bar(
            age_counts, x="age", y="count",
            labels={"age": "Age Group", "count": "Count"},
            title="Age Distribution"
        )
        dash_fig1.update_layout(title={'x': 0.46})
        dash_fig1.update_layout(height=450)
        st.plotly_chart(dash_fig1, use_container_width=True)

        # Customers per Risk Score
        risk_counts = segment["risk_score"].value_counts().reset_index()
        risk_counts.columns = ["risk_score", "count"]
        risk_counts = risk_counts.sort_values("risk_score")

        dash_fig2 = px.bar(
            risk_counts, x="count", y="risk_score", orientation="h",
            labels={"risk_score": "Risk Score", "count": "Customers"},
            title="Customers per Risk Score"
        )
        dash_fig2.update_layout(title={'x': 0.46})
        dash_fig2.update_layout(height=450)
        st.plotly_chart(dash_fig2, use_container_width=True)

    with col5:
        # Income Bracket Distribution
        income_counts = segment["income"].value_counts().reset_index()
        income_counts.columns = ["income", "count"]
        dash_fig3 = px.pie(
            income_counts, names="income", values="count",
            title="Income Bracket Distribution"
        )
        dash_fig3.update_layout(title={'x': 0.3})
        dash_fig3.update_layout(height=450)
        st.plotly_chart(dash_fig3, use_container_width=True)

        # Claim Outcome Breakdown
        outcome_counts = segment["outcome"].value_counts().reset_index()
        outcome_counts.columns = ["Outcome", "Count"]
        outcome_counts["Outcome"] = outcome_counts["Outcome"].map({0: "No Claim", 1: "Filed Claim"})

        dash_fig4 = px.pie(
            outcome_counts, names="Outcome", values="Count",
            title="Claim Outcome Distribution"
        )
        dash_fig4.update_layout(title={'x': 0.3})
        dash_fig4.update_layout(height=450)
        st.plotly_chart(dash_fig4, use_container_width=True)