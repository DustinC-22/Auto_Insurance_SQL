-- ===========================================================
-- risk_analysis.sql: Portfolio Risk and Claim Analysis Queries
-- ===========================================================
-- This file contains descriptive SQL queries to explore the distribution of 
-- claims and risk scores across key customer demographics and segments.
-- These queries help profile the insurance portfolio before and after risk scoring.
-- ===========================================================

USE auto_insurance_db;

-- 1. Claim Rate by Postal Code
-- Business Insight: Identify regional hotspots with higher claim rates.
SELECT c.postal_code,
       COUNT(*) AS total_customers,
       SUM(cl.outcome) AS total_claims,
       ROUND(SUM(cl.outcome) / COUNT(*), 2) AS claim_rate
FROM customers c
JOIN claims cl ON c.id = cl.id
GROUP BY c.postal_code
ORDER BY claim_rate DESC;

-- 2. Average Risk Score and Claim Rate by Income Bracket
-- Business Insight: Do lower or higher income brackets correlate with higher risk or claims?
SELECT c.income,
       ROUND(AVG(rs.risk_score), 2) AS avg_risk_score,
       ROUND(SUM(cl.outcome) / COUNT(*), 2) AS claim_rate,
       COUNT(*) AS total_customers
FROM customers c
JOIN risk_scores rs ON c.id = rs.id
JOIN claims cl ON c.id = cl.id
GROUP BY c.income
ORDER BY avg_risk_score DESC;

-- 3. Risk Score and Claim Rate by Gender
-- Business Insight: Assess gender-based risk differences.
SELECT c.gender,
       ROUND(AVG(rs.risk_score), 2) AS avg_risk_score,
       ROUND(SUM(cl.outcome) / COUNT(*), 2) AS claim_rate,
       COUNT(*) AS total_customers
FROM customers c
JOIN risk_scores rs ON c.id = rs.id
JOIN claims cl ON c.id = cl.id
GROUP BY c.gender
ORDER BY avg_risk_score DESC;

-- 4. Average Annual Mileage by Vehicle Type
-- Business Insight: Understand driving behaviour across vehicle types.
SELECT vehicle_type,
       ROUND(AVG(annual_mileage), 0) AS avg_annual_mileage,
       COUNT(*) AS total_vehicles
FROM vehicles
GROUP BY vehicle_type
ORDER BY avg_annual_mileage DESC;

-- 5. Claim Rate by Age Group
-- Business Insight: Which age groups are filing the most claims?
SELECT age,
       COUNT(*) AS total_customers,
       SUM(cl.outcome) AS total_claims,
       ROUND(SUM(cl.outcome) / COUNT(*), 2) AS claim_rate
FROM customers c
JOIN claims cl ON c.id = cl.id
GROUP BY age
ORDER BY claim_rate DESC;

-- 6. Risk Score vs. Claim Rate (Portfolio-Wide Summary)
-- Business Insight: Reinforce that higher risk scores align with higher claim rates.
SELECT risk_score,
       COUNT(*) AS total_customers,
       SUM(outcome) AS total_claims,
       ROUND(SUM(outcome) / COUNT(*), 2) AS claim_rate
FROM risk_scores rs
JOIN claims cl ON rs.id = cl.id
GROUP BY risk_score
ORDER BY risk_score DESC;

-- 7. Claim Rate by Age and Income
-- Business Insight: Identify how income level modifies risk across different age groups.
SELECT age, income, 
       COUNT(*) AS total_customers,
       SUM(cl.outcome) AS total_claims,
       ROUND(SUM(cl.outcome) / COUNT(*), 2) AS claim_rate
FROM customers c
JOIN claims cl ON c.id = cl.id
GROUP BY age, income
ORDER BY age, income;

-- 8. Claim Rate by Driving Experience
-- Business Insight: Show how increased driving experience correlates with lower claim rates.
SELECT driving_experience,
       COUNT(*) AS total_customers,
       SUM(cl.outcome) AS total_claims,
       ROUND(SUM(cl.outcome) / COUNT(*), 2) AS claim_rate
FROM driving_history d
JOIN claims cl ON d.id = cl.id
GROUP BY driving_experience
ORDER BY claim_rate DESC;

-- 9. Claim Rate and Mileage by Vehicle Year
-- Business Insight: Older vehicles have higher exposure and claim rates, supporting a vehicle age risk flag.
SELECT vehicle_year,
       COUNT(*) AS total_vehicles,
       ROUND(AVG(annual_mileage), 0) AS avg_annual_mileage,
       ROUND(SUM(cl.outcome) / COUNT(*), 2) AS claim_rate
FROM vehicles v
JOIN claims cl ON v.id = cl.id
GROUP BY vehicle_year
ORDER BY claim_rate DESC;

-- 10. Risk Score Distribution
-- Business Insight: Validate the risk score spread across the portfolio and check for over-concentration at certain scores.
SELECT risk_score,
       COUNT(*) AS num_customers
FROM risk_scores
GROUP BY risk_score
ORDER BY risk_score DESC;

-- 11. Claim Rate by Credit Score Bands
-- Business Insight: Break credit scores into meaningful bands and show clear risk stratification.
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