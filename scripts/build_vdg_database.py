import re
from pathlib import Path

import fitz
import pandas as pd

PDF_FOLDER = Path("data/pdfs")
OUTPUT_FILE = Path("data/vdg_motor_catalog.xlsx")


# -------------------------------
# Parse model name
# TM100B25
# -------------------------------
def parse_model(model):

    m = re.match(
        r"TM(\d+)([A-Z])(\d+)",
        model
    )

    if not m:
        return None

    return {
        "Drum_DIA_mm": int(m.group(1)),
        "Series": m.group(2),
        "Shaft_DIA_mm": int(m.group(3))
    }


# -------------------------------
# Parse one horsepower section
# -------------------------------
def process_section(
    section_text,
    hp,
    model,
    model_info,
    pdf_name
):

    rows = []

    # V + M/G pairs

    vmg_pairs = re.findall(
        r"(\d+)\s+([246])\/([A-Z0-9]+)",
        section_text
    )

    if not vmg_pairs:
        return rows

    # Belt Pull row

    belt_match = re.search(
        r"Belt Pull.*?\n(.*?)\n",
        section_text,
        re.S
    )

    pulls = []

    if belt_match:

        pulls = re.findall(
            r"\d+",
            belt_match.group(1)
        )

    # Drum RPM row

    rpm_match = re.search(
        r"Drum RPM.*?\n(.*?)\n",
        section_text,
        re.S
    )

    rpms = []

    if rpm_match:

        rpms = re.findall(
            r"\d+",
            rpm_match.group(1)
        )

    count = min(
        len(vmg_pairs),
        len(pulls),
        len(rpms)
    )

    for i in range(count):

        speed, pole, gear = vmg_pairs[i]

        rows.append({

            "Model":
                model,

            "Drum_DIA_mm":
                model_info["Drum_DIA_mm"],

            "Shaft_DIA_mm":
                model_info["Shaft_DIA_mm"],

            "Series":
                model_info["Series"],

            "Power_HP":
                hp,

            "V_ft_min":
                int(speed),

            "Pole":
                int(pole),

            "Gear_Code":
                gear,

            "Belt_Pull_lbf":
                int(pulls[i]),

            "Drum_RPM":
                int(rpms[i]),

            "Phase":
                3,

            "Frequency_Hz":
                60,

            "Source_PDF":
                pdf_name
        })

    return rows


# -------------------------------
# Process PDF
# -------------------------------
def process_pdf(pdf_path):

    rows = []

    model = pdf_path.stem.replace(
        "s_",
        ""
    )

    model_info = parse_model(
        model
    )

    if not model_info:
        return rows

    doc = fitz.open(
        pdf_path
    )

    text = ""

    for page in doc:

        text += (
            page.get_text()
            + "\n"
        )

    # Split by HP sections

    hp_sections = re.split(
        r"(\d+\.\d+\s*HP)",
        text
    )

    current_hp = None

    for block in hp_sections:

        hp_match = re.match(
            r"(\d+\.\d+)\s*HP",
            block
        )

        if hp_match:

            current_hp = float(
                hp_match.group(1)
            )

            continue

        if current_hp is None:
            continue

        rows.extend(

            process_section(
                block,
                current_hp,
                model,
                model_info,
                pdf_path.name
            )

        )

    return rows


# -------------------------------
# Main
# -------------------------------
def main():

    all_rows = []

    pdfs = sorted(
        PDF_FOLDER.glob(
            "*.pdf"
        )
    )

    print(
        f"Found {len(pdfs)} PDFs"
    )

    for pdf in pdfs:

        print(
            f"Processing {pdf.name}"
        )

        rows = process_pdf(
            pdf
        )

        all_rows.extend(
            rows
        )

    df = pd.DataFrame(
        all_rows
    )

    df = df.drop_duplicates()

    df.to_excel(
        OUTPUT_FILE,
        index=False
    )

    print()
    print(
        f"Saved {len(df)} rows"
    )

    print(
        OUTPUT_FILE
    )


if __name__ == "__main__":
    main()