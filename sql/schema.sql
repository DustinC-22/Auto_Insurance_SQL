-- ===========================================================
-- schema.sql: Database Schema for Auto Insurance Risk Analysis
-- ===========================================================
-- This script creates the database and core tables for the project.
-- It must be run before loading data or executing any analysis queries.
-- ===========================================================

-- 1. Create and Select the Database
CREATE DATABASE IF NOT EXISTS auto_insurance_db;
USE auto_insurance_db;

-- 2. Create Customers Table
-- Stores customer demographics, credit, and policyholder details.
CREATE TABLE IF NOT EXISTS customers (
    id INT PRIMARY KEY,
    age VARCHAR(20),
    gender VARCHAR(10),
    race VARCHAR(20),
    education VARCHAR(50),
    income VARCHAR(30),
    credit_score DECIMAL(5, 4),
    married BOOLEAN,
    children INT,
    postal_code VARCHAR(10)
);

-- 3. Create Vehicles Table
-- Stores vehicle ownership details and mileage.

CREATE TABLE IF NOT EXISTS vehicles (
    id INT PRIMARY KEY,
    vehicle_ownership BOOLEAN,
    vehicle_year VARCHAR(20),
    vehicle_type VARCHAR(20),
    annual_mileage INT
);

-- 4. Create Driving History Table
-- Stores driver experience and past driving violations.
CREATE TABLE IF NOT EXISTS driving_history (
    id INT PRIMARY KEY,
    driving_experience VARCHAR(20),
    speeding_violations INT,
    duis INT,
    past_accidents INT
);

-- 5. Create Claims Table
-- Stores the claim outcome for each customer.
CREATE TABLE IF NOT EXISTS claims (
    id INT PRIMARY KEY,
    outcome BOOLEAN COMMENT '1 = claim filed, 0 = no claim'
);

-- 6. Test Queries
-- Verify that all tables are created successfully.
SELECT * FROM customers LIMIT 10;
SELECT * FROM vehicles LIMIT 10;
SELECT * FROM driving_history LIMIT 10;
SELECT * FROM claims LIMIT 10;
