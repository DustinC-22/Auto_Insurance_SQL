-- ===========================================================
-- analytics.sql: Portfolio Risk and Performance Summaries
-- ===========================================================
-- This script contains summary-level queries designed to evaluate
-- the overall claim risk across the auto insurance portfolio and 
-- assess how well the risk scoring segments customers.
-- These queries are intended to power summary dashboards or reports.
-- ===========================================================

USE auto_insurance_db;

-- 1. Portfolio-Wide Claim Rate
-- Business Insight: Shows the overall claim rate across all customers.
SELECT COUNT(*) AS total_customers,
       SUM(outcome) AS total_claims,
       ROUND(SUM(outcome) / COUNT(*), 2) AS overall_claim_rate
FROM claims;

-- 2. Claim Rate for High-Risk Customers (Risk Score ≥ 3)
-- Business Insight: Evaluate claim rates among the highest risk segment.
SELECT COUNT(*) AS high_risk_customers,
       SUM(outcome) AS total_claims,
       ROUND(SUM(outcome) / COUNT(*), 2) AS claim_rate
FROM risk_scores rs
JOIN claims cl ON rs.id = cl.id
WHERE risk_score >= 3;

-- 3. Risk Score Segmentation Claim Performance
-- Business Insight: Show claim rates across simplified risk score categories.
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

-- 4. Risk Score Distribution Across Portfolio
-- Business Insight: What percentage of the portfolio falls into each risk score?
SELECT risk_score,
       COUNT(*) AS num_customers,
       ROUND(100 * COUNT(*) / (SELECT COUNT(*) FROM risk_scores), 1) AS pct_of_portfolio
FROM risk_scores
GROUP BY risk_score
ORDER BY risk_score DESC;

-- 5. Claim Rate Comparison: High Risk vs Low Risk
-- Business Insight: Directly compare claim rates between risk extremes.
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

-- 6. Risk Score vs. Total Claims Generated
-- Business Insight: Which risk scores are responsible for the most claims in total?
SELECT risk_score,
       SUM(outcome) AS total_claims,
       COUNT(*) AS total_customers,
       ROUND(SUM(outcome) / COUNT(*), 2) AS claim_rate
FROM risk_scores rs
JOIN claims cl ON rs.id = cl.id
GROUP BY risk_score
ORDER BY total_claims DESC;