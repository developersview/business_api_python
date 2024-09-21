# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 17:48:44 2024

@author: pcslg
"""

# database.py
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
