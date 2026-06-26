import re

from app.models.outline_drawing import OutlineDrawingFields


class OutlineParser:

    def parse(self, text: str) -> OutlineDrawingFields:

        txt = text.upper()

        fields = OutlineDrawingFields()

        self.extract_model(txt, fields)
        self.extract_face_width(txt, fields)
        self.extract_material(txt, fields)
        self.extract_profile(txt, fields)
        self.extract_power_entry(txt, fields)
        self.extract_rod_qty(txt, fields)
        self.extract_sprocket(txt, fields)
        self.extract_qty(txt, fields)

        self.extract_voltage(txt, fields)
        self.extract_hp(txt, fields)
        self.extract_speed(txt, fields)

        self.extract_gearcode(txt, fields)
        self.extract_oil(txt, fields)

        return fields

    def extract_model(self, txt, fields):

        m = re.search(
        r"^\s*([^\s-]+)-",
        txt,
        re.MULTILINE
    )

        if m:
            fields.model = m.group(1)

    def extract_face_width(self, txt, fields):

        m = re.search(
            r"L\s*=\s*(\d+)\s*MM",
            txt
        )

        if m:
            fields.face_width = (
                str(int(m.group(1))).zfill(4)
            )

    def extract_material(self, txt, fields):

        if "STAINLESS STEEL" in txt:
            fields.material = "SS"

        elif "MILD STEEL" in txt:
            fields.material = "MS"

    def extract_profile(self, txt, fields):

        if "FLAT FACE" in txt:
            fields.profile = "FF"

        elif "CROWN" in txt:
            fields.profile = "CR"

        elif "TRAPEZOID" in txt:
            fields.profile = "TR"

    def extract_power_entry(self, txt, fields):

        if "JUNCTION BOX" in txt:
            fields.power_entry = "JB"

        elif "CABLE" in txt:
            fields.power_entry = "CBL"

    def extract_rod_qty(self, txt, fields):

        m = re.search(
            r"(\d+)\s*ROD",
            txt
        )

        if m:
            fields.rod_qty = m.group(1)

    def extract_sprocket(self, txt, fields):

        m = re.search(
            r"(S\d+-\d+T)",
            txt
        )

        if m:
            fields.sprocket = m.group(1)

    def extract_qty(self, txt, fields):

        m = re.search(
            r"QTY\s*(\d+)",
            txt
        )

        if m:
            fields.sprocket_qty = m.group(1)

    def extract_voltage(self, txt, fields):

        m = re.search(
            r"(\d+)\s*NB",
            txt
        )

        if m:
            fields.voltage = m.group(1)

    def extract_hp(self, txt, fields):

        m = re.search(
            r"HP\s*=\s*([0-9.]+)",
            txt
        )

        if m:
            fields.horsepower = m.group(1)

    def extract_speed(self, txt, fields):

        m = re.search(
            r"V\s*=\s*([0-9.]+)",
            txt
        )

        if m:
            fields.speed_fpm = m.group(1)

    def extract_gearcode(self, txt, fields):

        m = re.search(
            r"GEARCODE\s*=\s*([A-Z0-9]+)",
            txt
        )

        if m:
            fields.gearcode = m.group(1)

    def extract_oil(self, txt, fields):

        m = re.search(
            r"FG\d+",
            txt
        )

        if m:
            fields.oil = m.group()