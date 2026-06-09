import sqlite3
from pathlib import Path
import pandas as pd
from pdf_parser import parse_model, parse_pdf


def create_database(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute('''
    CREATE TABLE IF NOT EXISTS motor_performance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        motor_model TEXT,
        shell_od_mm INTEGER,
        shaft_type TEXT CHECK(shaft_type IN ('A','B')),
        shaft_od_mm INTEGER,
        hp REAL,
        speed_ftmin INTEGER,
        belt_pull_lbf INTEGER,
        drum_rpm INTEGER,
        stator_poles INTEGER,
        gear_code TEXT,
        source_pdf TEXT,
        
        UNIQUE(motor_model, hp,speed_ftmin)
    )
    ''')
    conn.commit()
    return conn

def import_folder(pdf_folder, conn):

    for pdf_file in pdf_folder.glob("*.pdf"):

        print(f"Processing {pdf_file.name}")

        rows = parse_pdf(pdf_file)

        insert_rows(conn, rows)

def insert_rows(conn, rows):

    cur = conn.cursor()

    for row in rows:

        cur.execute("""
        INSERT INTO motor_performance (

            motor_model,
            shell_od_mm,
            shaft_type,
            shaft_od_mm,

            hp,
            speed_ftmin,
            belt_pull_lbf,
            drum_rpm,

            stator_poles,
            gear_code,
            source_pdf

        )
        VALUES (
            ?,?,?,?,?,?,?,?,?,?,?
        )

        ON CONFLICT(
            motor_model,
            hp,
            speed_ftmin
        )

        DO UPDATE SET

            belt_pull_lbf = excluded.belt_pull_lbf,
            drum_rpm      = excluded.drum_rpm,
            stator_poles  = excluded.stator_poles,
            gear_code     = excluded.gear_code,
            source_pdf    = excluded.source_pdf

        """,
        (
            row["motor_model"],
            row["shell_od_mm"],
            row["shaft_type"],
            row["shaft_od_mm"],

            row["hp"],
            row["speed_ftmin"],
            row["belt_pull_lbf"],
            row["drum_rpm"],

            row["stator_poles"],
            row["gear_code"],
            row["source_pdf"]
        ))

    conn.commit()

def convert_db_to_excel(db_path, excel_path=None):
    """
    Convert SQLite database table motor_performance to Excel.

    Parameters
    ----------
    db_path : str
        Full path to motors.db

    excel_path : str, optional
        Output Excel file path.
        If omitted, creates .xlsx beside the database.
    """

    db_path = Path(db_path)

    if not db_path.exists():
        raise FileNotFoundError(
            f"Database not found:\n{db_path}"
        )

    if excel_path is None:
        excel_path = db_path.with_suffix(".xlsx")

    print(f"Reading database: {db_path}")

    conn = sqlite3.connect(str(db_path))

    try:

        # Verify available tables
        tables = pd.read_sql_query(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            """,
            conn
        )

        print("Tables found:")
        print(tables)

        # Load motor data
        df = pd.read_sql_query(
            """
            SELECT *
            FROM motor_performance
            """,
            conn
        )

        print(f"\nRows loaded: {len(df)}")

        # Export
        df.to_excel(
            excel_path,
            index=False
        )

        print(f"\nExcel exported:")
        print(excel_path)

    finally:
        conn.close()

def record_exists(
        conn,
        motor_model,
        hp,
        speed_ftmin):

    cur = conn.cursor()

    cur.execute("""
        SELECT id
        FROM motor_performance
        WHERE motor_model = ?
        AND hp = ?
        AND speed_ftmin = ?
    """,
    (
        motor_model,
        hp,
        speed_ftmin
    ))

    return cur.fetchone() is not None

def update_record(
        conn,
        motor_model,
        hp,
        speed_ftmin,
        field_name,
        new_value):

    allowed_fields = {
        "belt_pull_lbf",
        "drum_rpm",
        "stator_poles",
        "gear_code",
        "source_pdf"
    }

    if field_name not in allowed_fields:
        raise ValueError(f"Invalid field: {field_name}")

    sql = f"""
        UPDATE motor_performance
        SET {field_name} = ?
        WHERE motor_model = ?
        AND hp = ?
        AND speed_ftmin = ?
    """

    conn.execute(
        sql,
        (
            new_value,
            motor_model,
            hp,
            speed_ftmin
        )
    )

    conn.commit()

def update_by_id(
        conn,
        record_id,
        updates):

    allowed = {
        "motor_model",
        "hp",
        "speed_ftmin",
        "belt_pull_lbf",
        "drum_rpm",
        "stator_poles",
        "gear_code",
        "source_pdf"
    }

    fields = []
    values = []

    for field, value in updates.items():

        if field not in allowed:
            raise ValueError(field)

        fields.append(f"{field}=?")
        values.append(value)

    values.append(record_id)

    sql = f"""
        UPDATE motor_performance
        SET {', '.join(fields)}
        WHERE id=?
    """

    conn.execute(sql, values)
    conn.commit()