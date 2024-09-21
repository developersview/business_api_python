# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 20:52:31 2024

@author: pcslg
"""

# Create a file named database.py
import pyodbc

def get_connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=157.20.51.186;"
        "DATABASE=AIC; "
        "UID=sa;"
        "PWD=cmrpkc@123#;"
    )
    conn = pyodbc.connect(conn_str)
    return conn


query = "SELECT TOP 3 * FROM [dbo].[MemMaster] WHERE ID = ?;"
# Example usage of the connection
if __name__ == "__main__":
    try:
        conn = get_connection()
        print("Connection successful!")
        id = input("Provide ID: ")

        # Example query
        cursor = conn.cursor()
        cursor.execute(query, id)

        # Fetch and print the results
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        # Close the connection and cursor
        cursor.close()
        conn.close()

    except pyodbc.Error as e:
        print(f"Error connecting to SQL Server: {e}")
