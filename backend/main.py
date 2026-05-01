# 🔥 Datadog APM (MUST be at top)
from ddtrace import patch_all
patch_all()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import time
import os
import logging

print("🔥 APP STARTED WITH NEW CODE")

# App Insights setup (kept as-is)
try:
    from opencensus.ext.azure.log_exporter import AzureLogHandler

    logger = logging.getLogger("app_insights")
    connection_string = os.getenv("APPINSIGHTS_CONNECTION_STRING")

    if connection_string:
        handler = AzureLogHandler(connection_string=connection_string)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        print("✅ App Insights configured")
        logger.info("App Insights configured")

    else:
        logger = logging.getLogger("fallback")
        logger.setLevel(logging.INFO)
        print("⚠️ No App Insights connection string")

except Exception as e:
    logger = logging.getLogger("fallback")
    logger.setLevel(logging.INFO)
    print(f"❌ App Insights failed: {e}")

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB connection
conn = None
for i in range(5):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "postgres"),
            database=os.getenv("DB_NAME", "waterproofing"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "password")
        )
        print("✅ Connected to DB")
        logger.info("DB connected")
        break
    except Exception as e:
        print("❌ DB retry...", e)
        logger.error("DB connection failed")
        time.sleep(2)

if conn:
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id SERIAL PRIMARY KEY,
        name TEXT,
        phone TEXT,
        issue TEXT
    )
    """)
    conn.commit()

class Request(BaseModel):
    name: str
    phone: str
    issue: str

@app.get("/")
def home():
    print("🔥 HOME API HIT")
    logger.info("Home API hit")
    return {"message": "Backend working 🚀"}

@app.post("/submit")
def submit_request(req: Request):
    print(f"🔥 SUBMIT API: {req.name}")
    logger.info("Submit API called")

    if not conn:
        return {"error": "DB not connected"}

    cursor.execute(
        "INSERT INTO requests (name, phone, issue) VALUES (%s, %s, %s)",
        (req.name, req.phone, req.issue)
    )
    conn.commit()

    return {"message": "Saved"}

@app.get("/requests")
def get_requests():
    print("🔥 GET REQUESTS API")
    logger.info("Get requests API")

    if not conn:
        return {"error": "DB not connected"}

    cursor.execute("SELECT * FROM requests")
    data = cursor.fetchall()
    return {"data": data}
