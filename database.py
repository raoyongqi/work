# database.py
import sqlite3
import pandas as pd
def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key1 TEXT,
        key2 TEXT,
        key3 INTEGER
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)

def insert_data(conn, data):
    columns = data[0].keys()
    columns_str = ', '.join(columns)
    placeholders = ', '.join(['?' for _ in columns])
    insert_sql = f"INSERT INTO data ({columns_str}) VALUES ({placeholders})"
    
    cursor = conn.cursor()
    for entry in data:
        values = tuple(entry[column] for column in columns)
        cursor.execute(insert_sql, values)
    conn.commit()

def fetch_all_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data")
    return cursor.fetchall()

def export_to_excel(conn, file_name):
    query = "SELECT * FROM data"
    df = pd.read_sql_query(query, conn)
    df.to_excel(file_name, index=False, engine='openpyxl')