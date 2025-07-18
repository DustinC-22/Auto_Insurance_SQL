# Auto Insurance Portfolio Risk Analysis (SQL-Based)

This project develops a SQL-powered risk scoring pipeline for an auto insurance portfolio using a synthetic dataset. The goal is to demonstrate SQL-first data modelling, risk flag creation, scoring logic, and risk-performance analysis. This project highlights how actuarial-style portfolio segmentation can be driven by SQL queries alone, transforming raw insurance data into actionable insights for fraud detection, underwriting, and pricing adjustments.

Access dashboard online via:
https://autoinsurancesql.streamlit.app/Dashboard

---

## Project Structure

```
├── datasets/
│   ├── raw/                      # Original Kaggle dataset
│   │   └── Car_Insurance_Claim.csv
│   ├── processed/                # Cleaned and split normalized tables
│   │   ├── customers.csv
│   │   ├── vehicles.csv
│   │   ├── driving_history.csv
│   │   └── claims.csv
│   └── data_cleaning.ipynb       # Data prep and splitting
│
├── sql/
│   ├── schema.sql                # Table creation statements
│   ├── risk_flags.sql            # Risk flag logic
│   ├── risk_scoring.sql          # Final risk scoring logic
│   ├── risk_analysis.sql         # Exploratory profiling queries
│   └── analytics.sql             # Portfolio and performance summaries
│
├── streamlit_app/                # Interactive analytics dashboard
|   ├── pages/
│   |   ├── 1_Data_Overview.py
│   |   ├── 2_Risk_Scoring.py
│   |   ├── 3_Risk_Summary.py
│   |   └── 4_Dashboard.py
|   ├── public/
|   ├── venv/
|   ├── app.py
|   ├── db_connection.py
|   └── requirements.txt    
```

---

## Objectives

- Normalize an auto insurance claims dataset into a clean SQL database schema.
- Create risk factor flags using SQL logic to represent driver behaviour, demographics, and vehicle profiles.
- Calculate a risk score by summing binary risk flags for each customer.
- Analyze how risk scores correlate with actual claim-filing rates.
- Segment the portfolio into actionable risk tiers using only SQL.
- Provide descriptive and performance summaries for fraud detection and pricing teams.
- Visualize portfolio insights interactively using Streamlit.

---

## Data Sources

- [Kaggle: Car Insurance Data](https://www.kaggle.com/datasets/sagnik1511/car-insurance-data/data)
  - `Car_Insurance_Claim.csv`
- Cleaned and split into:
  - `customers.csv`
  - `vehicles.csv`
  - `driving_history.csv`
  - `claims.csv`

---

## Tools & Techniques

- **SQL**: MySQL Workbench, `JOIN`, `CASE`, `GROUP BY`, `CREATE VIEW`, CTEs.
- **Streamlit**: Interactive dashboard with charts, filters, segment profiling.
- **Plotly**: Bar charts, pie charts, line graphs, heatmaps, and grouped visualizations.
- **Pandas**: CSV pre-processing.
- **Streamlit**: Used to host the MySQL database.
- Modular query design for flexible exploration and scoring pipelines.

---

## How to Run the SQL Pipeline

1. **Create tables**: Run `schema.sql` in your SQL environment.
2. **load data**: Run `load_data.sql` to import datasets (Ensure file paths are correct and `LOCAL INFILE` is enabled).
3. **Risk flags**: Run `risk_flags.sql` to generate flag logic.
4. **Score customers**: Execute `risk_scoring.sql` to generate the `risk_scores` view.
5. **Explore**: Use `risk_analysis.sql` and `analytics.sql` for segmentation and performance.

---

## Streamlit Dashboard

`streamlit_app/` contains a modular Streamlit dashboard broken into four interactive pages:

| Page                 | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| **Data Overview**    | High-level summary of the dataset, risk tiers, and data structure.          |
| **Risk Scoring**     | Explore scoring logic, heatmap of risk factor contribution.                 |
| **Risk Summary**     | Portfolio-wide KPIs, claim trends, gender/region risk, vehicle insights.    |
| **Dashboard**        | Dynamic segment filters to drill into behaviour, claims, and composition.   |

### To run locally:
```bash
cd streamlit_app
.\venv\Scripts\Activate 
streamlit run app.py
```
---
