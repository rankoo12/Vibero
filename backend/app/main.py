from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy
from app.core.database import SessionLocal
from app.core.database import Base, engine
from app.models import user, game # make sure this import is used
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Running lifespan startup")
    Base.metadata.create_all(bind=engine)
    yield



app = FastAPI(lifespan=lifespan)


# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust for frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"msg": "Vibero backend is running"}

@app.get("/favicon.ico")
async def favicon():
    return {}


