import pdfplumber
from pathlib import Path

def parse_pdf(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    model_match = re.search(
        r'(TM\d+[AB]\d+)\s+Drum Motor',
        text
    )

    if not model_match:
        raise ValueError(
            f"Cannot determine model from {pdf_file}"
        )

    model = model_match.group(1)

    model_info = parse_model(model)

    rows = extract_blocks(text)

    for row in rows:

        row["motor_model"] = model

        row["shell_od_mm"] = model_info["shell_od_mm"]
        row["shaft_type"] = model_info["shaft_type"]
        row["shaft_od_mm"] = model_info["shaft_od_mm"]

        row["source_pdf"] = Path(pdf_file).name

    return rows