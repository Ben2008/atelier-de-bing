from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.services.vdg_motor.database import search_motors, get_motor_by_id, get_motor_specifications, calculate_derived_specs

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/utilities/vdg-motor")
async def vdg_motor_page(
        request: Request,
        speed: int = 400,
        pull: int = 20
        ):

    results = search_motors(speed, pull)

    return templates.TemplateResponse(
    request=request,
    name="vdg_motor.html",
    context={
        "results": results,
        "speed": speed,
        "pull": pull
    }
    )


@router.get("/utilities/vdg-motor/view/{motor_id}")
async def motor_view_page(
        request: Request,
        motor_id: int
        ):
    """
    Display detailed motor specifications in motor_view page
    Splits specifications into Metric and Imperial groups
    Calculates derived specifications:
    - Vsynchronous, Vr, Gear Ratio
    - Unit conversions (using cal_ prefix fields if available)
    """
    
    motor = get_motor_by_id(motor_id)
    
    if not motor:
        return templates.TemplateResponse(
            request=request,
            name="motor_view.html",
            context={
                "motor": None,
                "error": "Motor not found"
            }
        )
    
    # Get specifications grouped by unit type
    metric_specs, imperial_specs = get_motor_specifications(motor_id)
    
    # Calculate derived specifications and unit conversions
    derived_specs = calculate_derived_specs(motor)
    
    return templates.TemplateResponse(
        request=request,
        name="motor_view.html",
        context={
            "motor": motor,
            "metric_specs": metric_specs,
            "imperial_specs": imperial_specs,
            "derived_specs": derived_specs,
            "error": None
        }
    )
