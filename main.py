# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 01:56:40 2024

@author: pcslg
"""

from fastapi import FastAPI, HTTPException, Depends, Security, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
import database
import uuid

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy user data (in a real app, you'd fetch this from a database)
user_details = {
    "admin": {
        "username": "admin",
        "full_name": "User Name",
        "email": "user@example.com",
        "hashed_password": "Sept23092024!@#",  # Store hashed passwords
        "disabled": False,
        "token": None
    }
}


# Function to verify the user's credentials
def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password  # Replace with a proper hash check

# Function to authenticate the user
def authenticate_user(username: str, password: str):
    user = user_details.get(username)
    if not user:
        print("User not found")
        return False
    if not verify_password(password, user_details["admin"]["hashed_password"]):
        print("Password does not match")
        return False
    return user

# Dependency to get the current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    usertoken = user_details["admin"]["token"]  # In a real app, validate the token
    #print(usertoken)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    elif usertoken != token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return usertoken

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
    ADD2: Optional[str]  # Allow ADD2 to be Optional
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

# Endpoint to get a token
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # Create a new token
    token = str(uuid.uuid4())
    user_details["admin"]["token"] = token
    #print(user_details)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/items")
async def fetch_all_rows_by_different_filters(
    item_id: Optional[int] = Query(None, description="Filter by item ID"),
    city: Optional[str] = Query(None, description="Filter by city"),
    district: Optional[str] = Query(None, description="Filter by district"),
    state: Optional[str] = Query(None, description="Filter by state"),
    pin: Optional[str] = Query(None, description="Filter by pin"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    bloodgr: Optional[str] = Query(None, description="Filter by blood group"),
    block: Optional[str] = Query(None, description="Filter by block"),
    booth: Optional[str] = Query(None, description="Filter by booth"),
    prof: Optional[str] = Query(None, description="Filter by profession"),
    current_user: dict = Depends(get_current_user)
):
    conn = database.get_connection()
    cursor = conn.cursor()

    # Construct the SQL query with conditional filters
    query = "SELECT * FROM [dbo].[MemMaster] WHERE 1=1"
    params = []

    if item_id:
        query += " AND ID = ?"
        params.append(item_id)

    if city:
        query += " AND CITY = ?"
        params.append(city)
    
    if district:
        query += " AND DISTRICT = ?"
        params.append(district)

    if state:
        query += " AND STATE = ?"
        params.append(state)
        
    if pin:
        query += " AND PIN = ?"
        params.append(pin)

    if gender:
        query += " AND GENDER = ?"
        params.append(gender)
        
    if bloodgr:
        query += " AND BLOODGR = ?"
        params.append(bloodgr)
    
    if block:
        query += " AND BLOCK = ?"
        params.append(block)
        
    if booth:
        query += " AND BOOTH = ?"
        params.append(booth)
    
    if prof:
        query += " AND PROF = ?"
        params.append(prof)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    if rows:
        items = [Item(
            ID=row[0],
            JDATE=row[1].strftime("%Y-%m-%d"), # Convert JDATE to string 
            REFID=row[2],
            MNAME=row[3],
            FNAME=row[4],
            QUAL=row[5],
            BLOODGR=row[6],
            GENDER=row[7],
            ADD1=row[8],
            ADD2=row[9] if row[9] is not None else None,
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
        ) for row in rows]
        return items
    else:
        raise HTTPException(status_code=404, detail="No items found")



#fetch row based on id
@app.get("/items/id/{item_id}")
async def fetch_all_rows_by_id(item_id: int, current_user: dict = Depends(get_current_user)):
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

#fetch rows based on city        
@app.get("/items/city/{city_name}")
async def fetch_all_rows_by_city(city_name: str, current_user: dict = Depends(get_current_user)):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.MemMaster WHERE CITY = ?", city_name)
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

#fetch rows based on district
@app.get("/items/district/{district_name}")
async def fetch_all_rows_by_district(district_name: str, current_user: dict = Depends(get_current_user)):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.MemMaster WHERE DISTRICT = ?", district_name)
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
        
#fetch rows based on pin        
@app.get("/items/pin/{pin}")
async def fetch_all_rows_by_pin(pin: str, current_user: dict = Depends(get_current_user)):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.MemMaster WHERE PIN = ?", pin)
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

#fetch rows based on state     
@app.get("/items/state/{state_name}")
async def fetch_all_rows_by_state(state: str, current_user: dict = Depends(get_current_user)):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.MemMaster WHERE STATE = ?", state)
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
        
#fetch rows based on gender        
@app.get("/items/gender/{gender}")
async def fetch_all_rows_by_gender(gender: str, current_user: dict = Depends(get_current_user)):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.MemMaster WHERE GENDER = ?", gender)
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
        