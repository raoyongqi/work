# main.py
from fastapi import FastAPI
from routers.data_router import router
from database import create_connection, create_table
import os

# 数据目录和数据库文件路径
DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "data.db")

# Define the lifespan function as an async generator
async def lifespan(app: FastAPI):
    # Application startup logic
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    conn = create_connection(DB_FILE)
    create_table(conn)
    conn.close()
    
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
