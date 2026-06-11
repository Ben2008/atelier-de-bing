from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).parent

DB_NAME = BASE_DIR / "outline_drawing.db"
EXCEL_NAME = BASE_DIR / "outline_drawing.xlsx"

conn = sqlite3.connect(DB_NAME)

# Get all table names
tables = pd.read_sql_query(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
    """,
    conn
)

with pd.ExcelWriter(EXCEL_NAME, engine="openpyxl") as writer:

    for table in tables["name"]:

        # Skip SQLite internal tables
        if table.startswith("sqlite_"):
            continue

        print(f"Exporting {table}")

        df = pd.read_sql_query(
            f"SELECT * FROM {table}",
            conn
        )

        # Excel sheet names max 31 chars
        sheet_name = table[:31]

        df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False
        )

conn.close()

print(f"\nExcel exported successfully:")
print(EXCEL_NAME)