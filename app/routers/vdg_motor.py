from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.services.vdg_motor.database import search_motors

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/utility/vdg-motor")
async def vdg_motor_page(
        request: Request,
        speed: int = 400,
        pull: int = 20
):

    results = search_motors(
        speed,
        pull
    )

    return templates.TemplateResponse(
    request=request,
    name="vdg_motor.html",
    context={
        "results": results,
        "speed": speed,
        "pull": pull
    }
)
