from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import time
import os
import logging

# 🔥 App Insights setup (SAFE initialization)
try:
    from opencensus.ext.azure.log_exporter import AzureLogHandler

    logger = logging.getLogger("app_insights")
    connection_string = os.getenv("APPINSIGHTS_CONNECTION_STRING")

    if connection_string:
        logger.addHandler(
            AzureLogHandler(connection_string=connection_string)
        )
        logger.setLevel(logging.INFO)
        logger.info("Application Insights configured successfully ✅")
    else:
        logger = logging.getLogger("fallback")
        logger.setLevel(logging.INFO)
        logger.info("App Insights connection string not found ⚠️")

except Exception as e:
    logger = logging.getLogger("fallback")
    logger.setLevel(logging.INFO)
    logger.error(f"App Insights setup failed: {str(e)}")

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ DB connection with retry
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
        logger.info("Connected to DB successfully")
        break
    except Exception as e:
        print("DB not ready, retrying...", e)
        logger.error(f"DB connection failed: {str(e)}")
        time.sleep(3)

# ❗ Handle failure safely
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
else:
    print("❌ DB connection failed. Backend running without DB")
    logger.error("DB connection failed after retries")

# Request model
class Request(BaseModel):
    name: str
    phone: str
    issue: str

# APIs
@app.get("/")
def home():
    logger.info("Home API hit")
    return {"message": "Backend running with DB 🚀"}

@app.post("/submit")
def submit_request(req: Request):
    logger.info(f"Submit API called with name={req.name}")

    if not conn:
        logger.error("Submit failed - DB not connected")
        return {"error": "DB not connected"}

    cursor.execute(
        "INSERT INTO requests (name, phone, issue) VALUES (%s, %s, %s)",
        (req.name, req.phone, req.issue)
    )
    conn.commit()

    logger.info("Data inserted successfully into DB")
    return {"message": "Saved to DB ✅"}

@app.get("/requests")
def get_requests():
    logger.info("Get requests API called")

    if not conn:
        logger.error("Fetch failed - DB not connected")
        return {"error": "DB not connected"}

    cursor.execute("SELECT * FROM requests")
    data = cursor.fetchall()

    logger.info(f"Fetched {len(data)} records")
    return {"data": data}
