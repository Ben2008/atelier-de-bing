import re

def parse_model(model):
    """
    TM100B25
    TM138A35
    """

    m = re.match(r"TM(\d+)([AB])(\d+)", model)

    if not m:
        raise ValueError(f"Invalid model name: {model}")

    return {
        "shell_od_mm": int(m.group(1)),
        "shaft_type": m.group(2),
        "shaft_od_mm": int(m.group(3))
    }