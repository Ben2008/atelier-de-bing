from dataclasses import dataclass


@dataclass
class OutlineDrawingFields:
    model: str = ""
    face_width: str = ""

    material: str = ""
    profile: str = ""

    power_entry: str = ""

    rod_qty: str = ""
    sprocket_qty: str = ""

    sprocket: str = ""
    belt_type: str = ""

    voltage: str = ""
    horsepower: str = ""
    speed_fpm: str = ""

    gearcode: str = ""

    oil: str = ""