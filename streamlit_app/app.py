import streamlit as st

st.set_page_config(page_title="Auto Insurance Risk Dashboard", layout="wide")

left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("streamlit_app/public/Corbett_Insurance.png", width=500)

st.title("Auto Insurance Risk & Claims Dashboard")
st.markdown("### A SQL-Driven Portfolio Analysis Tool")

st.markdown("""
This interactive dashboard explores a synthetic auto insurance dataset to identify claim risk patterns, evaluate customer segments, and support fraud mitigation strategies using a custom risk scoring system developed in SQL.

### **App Structure**
Use the sidebar to explore the following sections:
- Data Overview – Portfolio-wide metrics and exploratory visualizations
- Risk Scoring – SQL logic behind score construction and flag analysis
- Risk Summary – Risk band performance, distributions, and business insights
- Dashboard – Filter and analyze customer subgroups
                        
---

### **Project Objectives**
- Build SQL views and queries to identify high-risk customers based on behaviour and demographics
- Profile claim patterns across income, age, vehicle, and location segments
- Design a transparent scoring system for explainable risk analysis
- Visualize key trends to support business recommendations

---

### **Key Findings**
- Young drivers and customers with low credit are disproportionately represented in high-risk claims
- Risk scores between 3–5 correlate with over 3× the claim rate of lower scores
- Certain postal codes and vehicle types exhibit elevated exposure and claim frequency
- Credit score and driving history are highly predictive when combined

---

### **Business Recommendations**
- Introduce tiered pricing or underwriting rules for customers with risk scores ≥ 3
- Prioritize manual review of high-score customers with recent claims
- Consider credit improvement incentives to reduce long-term claim risk
- Use regional data to inform local fraud detection efforts
""")