import pdfplumber
from pathlib import Path
import re

def parse_model(model):
    """
    TM100B25
    TM138A35
    """
    #stem = Path(model).stem
    m = re.search(r"TM(\d+)([AB])(\d+)",model)
    #m = re.match(r"TM(\d+)([AB])(\d+)", model)
    print(m)

    if not m:
        raise ValueError(f"Invalid model name: {model}")

    return {
        "shell_od_mm": int(m.group(1)),
        "shaft_type": m.group(2),
        "shaft_od_mm": int(m.group(3))
    }

def extract_blocks(text):

    rows = []

    hp_matches = list(
        re.finditer(r'(\d+\.\d+)\s+HP', text)
    )

    for i, hp_match in enumerate(hp_matches):

        hp = float(hp_match.group(1))

        start = hp_match.end()

        end = (
            hp_matches[i + 1].start()
            if i + 1 < len(hp_matches)
            else len(text)
        )

        section = text[start:end]

        pattern = (
            r'V \(ft/min\) M/G (.*?)'
            r'Belt Pull \(lbf\) (.*?)'
            r'Drum RPM (.*?)(?='
            r'V \(ft/min\) M/G|'
            r'TM\d+[AB]\d+ Drum Motor|'
            r'$)'
        )

        matches = re.findall(
            pattern,
            section,
            flags=re.S
        )

        for speed_text, pull_text, rpm_text in matches:

            speed_pairs = re.findall(
                r'(\d+)\s+(\d+/(?:S2|S3|PL2|PL3))',
                speed_text
            )

            pulls = [
                int(x)
                for x in re.findall(r'\d+', pull_text)
            ]

            rpms = [
                int(x)
                for x in re.findall(r'\d+', rpm_text)
            ]

            count = min(
                len(speed_pairs),
                len(pulls),
                len(rpms)
            )

            for idx in range(count):

                speed = int(speed_pairs[idx][0])

                mg = speed_pairs[idx][1]

                poles, gear = mg.split('/')

                rows.append({
                    "hp": hp,
                    "speed_ftmin": speed,
                    "belt_pull_lbf": pulls[idx],
                    "drum_rpm": rpms[idx],
                    "stator_poles": int(poles),
                    "gear_code": gear
                })

    return rows

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

