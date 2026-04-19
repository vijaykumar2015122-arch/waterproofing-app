from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import time
import os

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ DB connection with retry using environment variables
conn = None
for i in range(10):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "postgres"),
            database=os.getenv("DB_NAME", "waterproofing"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "password")
        )
        print("Connected to DB ✅")
        break
    except Exception as e:
        print("DB not ready, retrying...", e)
        time.sleep(3)

# ❗ Handle failure safely
if conn:
    cursor = conn.cursor()
    # Create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id SERIAL PRIMARY KEY,
        name TEXT,
        phone TEXT,
        issue TEXT
    )
    """)
    conn.commit()
else:
    print("❌ DB connection failed. Backend running without DB")

# Request model
class Request(BaseModel):
    name: str
    phone: str
    issue: str

# APIs
@app.get("/")
def home():
    return {"message": "Backend running with DB 🚀"}

@app.post("/submit")
def submit_request(req: Request):
    if not conn:
        return {"error": "DB not connected"}
    cursor.execute(
        "INSERT INTO requests (name, phone, issue) VALUES (%s, %s, %s)",
        (req.name, req.phone, req.issue)
    )
    conn.commit()
    return {"message": "Saved to DB ✅"}

@app.get("/requests")
def get_requests():
    if not conn:
        return {"error": "DB not connected"}
    cursor.execute("SELECT * FROM requests")
    data = cursor.fetchall()
    return {"data": data}
