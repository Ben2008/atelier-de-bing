from fastapi import APIRouter
router = APIRouter(prefix="/mechanical", tags=["Mechanical Design"])

@router.get("/")
def mechanical_home():
    return {"module": "Mechanical Design"}
