-- ===========================================================
-- risk_flags.sql: Risk Factor Queries for Auto Insurance Analysis
-- ===========================================================
-- This script creates individual risk flags for key behavioural,
-- demographic, and vehicle-related attributes associated with claim risk.
-- These queries serve as the building blocks of the overall risk scoring system.
-- ===========================================================

USE auto_insurance_db;

-- 1. Speeding Risk Flag
-- Business Insight: Customers with frequent speeding violations are higher claim risks.
SELECT id,
       speeding_violations,
       CASE
           WHEN speeding_violations > 5 THEN 1
           ELSE 0
       END AS speeding_risk
FROM driving_history;

-- 2. DUI Risk Flag
-- Business Insight: Any history of DUIs significantly increases claim risk.
SELECT id,
       duis,
       CASE
           WHEN duis >= 1 THEN 1
           ELSE 0
       END AS dui_risk
FROM driving_history;

-- 3. Low Credit Score Risk Flag
-- Business Insight: Customers with low credit scores may exhibit higher financial or behavioural risk.
SELECT id,
       credit_score,
       CASE
           WHEN credit_score < 0.5 THEN 1
           ELSE 0
       END AS low_credit_risk
FROM customers;

-- 4. Vehicle Age & Mileage Risk Flag
-- Business Insight: Older vehicles with high mileage face greater mechanical and safety risks.
SELECT id,
       vehicle_year,
       annual_mileage,
       CASE
           WHEN vehicle_year = 'before 2015' AND annual_mileage > 15000 THEN 1
           ELSE 0
       END AS vehicle_risk
FROM vehicles;

-- 5. Young & Inexperienced Driver Risk Flag
-- Business Insight: Young drivers with limited experience are more likely to file claims.
SELECT c.id,
       c.age,
       d.driving_experience,
       CASE
           WHEN c.age = '16-25' AND d.driving_experience = '0-9y' THEN 1
           ELSE 0
       END AS young_driver_risk
FROM customers c
JOIN driving_history d ON c.id = d.id;