-- ===========================================================
-- load_data.sql: Load CSV Data
-- ===========================================================
-- Before running:
-- 1. Make sure LOCAL INFILE is enabled in your MySQL server/client.
-- 2. Replace the file paths below with the full path to your local CSVs.
--    Windows  : 'C:/Users/YourName/Path/to/...'
--    Mac/Linux: '/Users/YourName/Path/to/...'
-- 3. Ensure the tables have already been created (see schema.sql).
-- ===========================================================

USE auto_insurance_db;

-- Load Customers
LOAD DATA LOCAL INFILE '/absolute/path/to/datasets/processed/customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Load Vehicles
LOAD DATA LOCAL INFILE '/absolute/path/to/datasets/processed/vehicles.csv'
INTO TABLE vehicles
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Load Driving History
LOAD DATA LOCAL INFILE '/absolute/path/to/datasets/processed/driving_history.csv'
INTO TABLE driving_history
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Load Claims
LOAD DATA LOCAL INFILE '/absolute/path/to/datasets/processed/claims.csv'
INTO TABLE claims
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;