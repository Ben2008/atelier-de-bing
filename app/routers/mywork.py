from fastapi import APIRouter
router = APIRouter(prefix="/mywork", tags=["MyWork"])

@router.get("/")
def mywork_home():
    return {"module": "MyWork"}
