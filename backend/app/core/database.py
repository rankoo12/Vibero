import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

# Retry loop
MAX_RETRIES = 10
RETRY_INTERVAL = 2

for attempt in range(MAX_RETRIES):
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # ✅ use `text()` here
        break
    except OperationalError as e:
        print(f"[DB RETRY] PostgreSQL not ready ({attempt+1}/{MAX_RETRIES})...")
        time.sleep(RETRY_INTERVAL)
else:
    raise Exception("❌ Failed to connect to the database after multiple retries.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
