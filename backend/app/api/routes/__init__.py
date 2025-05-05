from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {"msg": "Vibero API is running"}
