import re

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