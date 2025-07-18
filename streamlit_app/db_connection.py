import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="auto-insurance-db.czy66ik2ez8d.us-east-2.rds.amazonaws.com",
        user="admin",
        password="Admin123",
        database="auto_insurance_db",
        port=3306
    )