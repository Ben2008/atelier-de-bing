from dataclasses import asdict

from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.services.utilities.outline_parser import OutlineParser

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)

parser = OutlineParser()


class ParseRequest(BaseModel):
    request_text: str


# ==================================================
# Page
# ==================================================

@router.get(
    "/utilities/outline-drawing",
    response_class=HTMLResponse
)
async def outline_drawing_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name= "outline_drawing.html",
        context=
        {
            "request": request
        }
    )

# ==================================================
# API
# ==================================================

@router.post("/api/outline-drawing/parse")
async def parse_outline(req: ParseRequest):

    result = parser.parse(
        req.request_text
    )

    return asdict(result)