# routers/data_router.py
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from database import create_connection, insert_data, fetch_all_data, export_to_excel
import os

router = APIRouter()

# 定义数据目录
DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "data.db")
EXCEL_FILE = os.path.join(DATA_DIR, "data.xlsx")

@router.post("/load-json/")
def load_json():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
        
        if not data:
            raise HTTPException(status_code=400, detail="JSON data is empty")

        conn = create_connection(DB_FILE)
        insert_data(conn, data)
        conn.close()
        return {"status": "success", "message": "Data loaded into database"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data/")
def get_data():
    try:
        conn = create_connection(DB_FILE)
        rows = fetch_all_data(conn)
        conn.close()
        return {"data": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download-db/")
def download_db():
    try:
        return FileResponse(DB_FILE, media_type='application/octet-stream', filename="data.db")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export-excel/")
def export_excel():
    try:
        conn = create_connection(DB_FILE)
        export_to_excel(conn, EXCEL_FILE)
        conn.close()
        return FileResponse(EXCEL_FILE, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename="data.xlsx")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
