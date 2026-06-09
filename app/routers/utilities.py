from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
router=APIRouter(prefix="/utilities", tags=["Utilities"])
templates=Jinja2Templates(directory="app/templates")
@router.get("/")
def utilities_home(request: Request):
    return templates.TemplateResponse(request=request,name="utilities.html",context={})
