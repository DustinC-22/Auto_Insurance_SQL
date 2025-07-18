-- ===========================================================
-- risk_scoring.sql: Risk Score Calculation and Portfolio Summary
-- ===========================================================
-- This script creates the combined risk scoring view and summarizes risk
-- across the auto insurance portfolio. Risk scores are calculated by summing
-- binary flags for each customer based on key risk factors.
-- ===========================================================

USE auto_insurance_db;

-- 1. Create Risk Scores View
-- Combines all individual risk flags into a total risk score for each customer.
CREATE OR REPLACE VIEW risk_scores AS
WITH speeding_flag AS (
    -- Speeding Risk: Flag customers with > 5 speeding violations
    SELECT id,
           CASE WHEN speeding_violations > 5 THEN 1 ELSE 0 END AS speeding_risk
    FROM driving_history
),
dui_flag AS (
    -- DUI Risk: Flag customers with at least 1 DUI
    SELECT id,
           CASE WHEN duis >= 1 THEN 1 ELSE 0 END AS dui_risk
    FROM driving_history
),
credit_flag AS (
    -- Low Credit Risk: Flag customers with credit score below 0.5
    SELECT id,
           CASE WHEN credit_score < 0.5 THEN 1 ELSE 0 END AS low_credit_risk
    FROM customers
),
vehicle_flag AS (
    -- Vehicle Risk: Flag customers with old vehicles and high mileage
    SELECT id,
           CASE WHEN vehicle_year = 'before 2015' AND annual_mileage > 15000 THEN 1 ELSE 0 END AS vehicle_risk
    FROM vehicles
),
young_driver_flag AS (
    -- Young & Inexperienced Driver Risk: Flag young drivers with little experience
    SELECT c.id,
           CASE WHEN c.age = '16-25' AND d.driving_experience = '0-9y' THEN 1 ELSE 0 END AS young_driver_risk
    FROM customers c
    JOIN driving_history d ON c.id = d.id
)

SELECT c.id,
       s.speeding_risk,
       d.dui_risk,
       cr.low_credit_risk,
       v.vehicle_risk,
       y.young_driver_risk,
       -- Sum of all risk flags creates the total risk score
       (s.speeding_risk + d.dui_risk + cr.low_credit_risk + v.vehicle_risk + y.young_driver_risk) AS risk_score
FROM customers c
LEFT JOIN speeding_flag s ON c.id = s.id
LEFT JOIN dui_flag d ON c.id = d.id
LEFT JOIN credit_flag cr ON c.id = cr.id
LEFT JOIN vehicle_flag v ON c.id = v.id
LEFT JOIN young_driver_flag y ON c.id = y.id;

-- 2. Test the Risk Scores View
-- Verify that risk scores and component flags are generated correctly.
SELECT * FROM risk_scores LIMIT 10;

-- 3. Portfolio Summary: Risk Score vs. Claim Rate
-- Business Insight: Higher risk scores correlate with higher claim rates.
SELECT risk_score,
       COUNT(*) AS total_customers,
       SUM(outcome) AS total_claims,
       ROUND(SUM(outcome) / COUNT(*), 2) AS claim_rate
FROM risk_scores rs
JOIN claims c ON rs.id = c.id
GROUP BY risk_score
ORDER BY risk_score DESC;

-- 4. Example High-Risk Customers
-- Business Insight: List the highest risk customers for potential review.
SELECT rs.id, risk_score, outcome
FROM risk_scores rs
JOIN claims c ON rs.id = c.id
ORDER BY risk_score DESC, outcome DESC
LIMIT 20;