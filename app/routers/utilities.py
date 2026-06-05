from fastapi import APIRouter
router = APIRouter(prefix="/utilities", tags=["Utilities"])

@router.get("/")
def utilities_home():
    return {"module": "Utilities"}
