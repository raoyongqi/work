from fastapi import FastAPI
from routers.data_router import router
from database import create_connection, create_table, insert_data
import os
import json

# 数据目录和数据库文件路径
DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "data.db")
JSON_FILE = os.path.join(DATA_DIR, "data.json")  # Ensure this path is correct

# Define the lifespan function as an async generator
async def lifespan(app: FastAPI):
    # Application startup logic
    os.makedirs(DATA_DIR, exist_ok=True)  # Create data directory if it doesn't exist
    
    # Open database connection and create table
    conn = create_connection(DB_FILE)
    create_table(conn)
    
    # Insert JSON data into the database
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            data = json.load(file)
            insert_data(conn, data)
    
    conn.close()  # Close connection after operations are complete

    # Yield control to FastAPI
    try:
        yield
    finally:
        # Application shutdown logic (if needed)
        pass

# Create the FastAPI app with the lifespan function
app = FastAPI(lifespan=lifespan)

# Include the router with endpoints
app.include_router(router)
