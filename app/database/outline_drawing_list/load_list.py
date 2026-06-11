from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).parent
DB_NAME = BASE_DIR / "outline_drawing.db"

VALID_PREFIXES = (
    "TM",
    "RTM",
    "TBCW",
    "TBCCW",
    "STM",
    "TMD"
)

conn = sqlite3.connect(DB_NAME)

total_lines = 0
accepted = 0
rejected_extension = 0
rejected_prefix = 0

for file_name, source in [

    (BASE_DIR / "MS_list.csv", "MS"),
    (BASE_DIR / "SS_list.csv", "SS")

]:

    print(f"\nProcessing: {file_name.name}")

    with open(file_name, "r", encoding="utf-8", errors="ignore") as f:

        for line in f:

            total_lines += 1

            line = line.strip()

            if not line:
                continue

            # Extract filename from full path
            drawing_file = Path(line).name

            # Must have extension
            if "." not in drawing_file:
                continue

            # DWG only
            if Path(drawing_file).suffix.lower() != ".dwg":
                rejected_extension += 1
                continue

            drawing_name = Path(drawing_file).stem

            # Valid motor prefixes only
            if not drawing_name.upper().startswith(VALID_PREFIXES):
                rejected_prefix += 1
                continue

            conn.execute("""
            INSERT OR IGNORE INTO drawing_master
            (
                drawing_name,
                file_path,
                source_list
            )
            VALUES (?, ?, ?)
            """,
            (
                drawing_name,
                line,
                source
            ))

            accepted += 1

conn.commit()
conn.close()

print("\n========== IMPORT SUMMARY ==========")
print(f"Total lines read      : {total_lines}")
print(f"Accepted drawings     : {accepted}")
print(f"Rejected extension    : {rejected_extension}")
print(f"Rejected prefix       : {rejected_prefix}")
print("====================================")
print("Import complete.")