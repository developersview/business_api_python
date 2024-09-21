# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 01:56:40 2024

@author: pcslg
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import database

app = FastAPI()

class Item(BaseModel):
    ID: int
    JDATE: str = None
    REFID: int = None
    MNAME: str = None
    FNAME: str = None
    QUAL: str = None
    BLOODGR: str = None
    GENDER: str = None
    ADD1: str = None
    ADD2: Optional[str]  # Allow ADD2 to be None
    BLOCK: str = None
    WARD: str = None
    BOOTH: str = None
    CITY: str = None
    DISTRICT: str = None
    STATE: str = None
    PIN: str = None
    EMAIL: str = None
    TELE1: str = None
    PROF: Optional[str]  # Handle as optional
    PROF2: Optional[str]  # Handle as optional
    
query_to_fetch_all_rows = "SELECT * FROM [dbo].[MemMaster];"
query_to_fetch_rows_by_id = "SELECT * FROM [dbo].[MemMaster] WHERE [ID] = ?"

@app.get("/")
def read_description():
    return {"description":"This is an API to retrieve data from MemMaster table from AIC database"}

@app.get("/items")
def fetch_all_rows():
    conn = database.get_connection();
    cursor = conn.cursor();
    cursor.execute(query_to_fetch_all_rows)
    rows = cursor.fetchall()
    if rows:
        items = [Item(
            ID = row[0],
            JDATE = row[1].strftime("%Y-%m-%d"), # Convert JDATE to string 
            REFID = row[2],
            MNAME = row[3],
            FNAME = row[4],
            QUAL = row[5],
            BLOODGR = row[6],
            GENDER = row[7],
            ADD1 = row[8],
            ADD2=row[9] if row[9] is not None else None,
            BLOCK = row[10],
            WARD = row[11],
            BOOTH = row[12],
            CITY = row[13],
            DISTRICT = row[14],
            STATE = row[15],
            PIN = row[16],
            EMAIL = row[17],
            TELE1 = row[18],
            PROF = row[19],
            PROF2 = row[20]
        ) for row in rows]
        return items
    else:
        raise HTTPException(status_code=404, detail="No items found")

@app.get("/items/{item_id}")
def fetch_all_rows_by_id(item_id: int):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.MemMaster WHERE ID = ?", item_id)
    row = cursor.fetchone()
    if row:
        return Item(
            ID=row[0],
            JDATE=row[1].strftime("%Y-%m-%d"), # Convert JDATE to string 
            REFID=row[2],
            MNAME=row[3],
            FNAME=row[4],
            QUAL=row[5],
            BLOODGR=row[6],
            GENDER=row[7],
            ADD1=row[8],
            ADD2=row[9],
            BLOCK=row[10],
            WARD=row[11],
            BOOTH=row[12],
            CITY=row[13],
            DISTRICT=row[14],
            STATE=row[15],
            PIN=row[16],
            EMAIL=row[17],
            TELE1=row[18],
            PROF=row[19],
            PROF2=row[20]
        )
    else:
        raise HTTPException(status_code=404, detail="Item not found")