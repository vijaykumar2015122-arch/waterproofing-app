from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import time

app = FastAPI()

# ✅ CORS FIX (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Wait for DB connection
conn = None
for i in range(10):
    try:
        conn = psycopg2.connect(
            host="postgres-db",
            database="waterproofing",
            user="admin",
            password="admin"
        )
        print("Connected to DB ✅")
        break
    except:
        print("DB not ready, retrying...")
        time.sleep(2)

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
    cursor.execute(
        "INSERT INTO requests (name, phone, issue) VALUES (%s, %s, %s)",
        (req.name, req.phone, req.issue)
    )
    conn.commit()
    return {"message": "Saved to DB ✅"}

@app.get("/requests")
def get_requests():
    cursor.execute("SELECT * FROM requests")
    data = cursor.fetchall()
    return {"data": data}
