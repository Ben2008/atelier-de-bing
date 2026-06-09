from pdf_parser import parse_model, parse_pdf
from pathlib import Path
from database import create_database, insert_rows, convert_db_to_excel, import_folder
import sqlite3

"""
if __name__ == "__main__":
    base_dir = Path(__file__).parent
    pdf_file = base_dir / "pdfs" / "s_TM100B25.pdf"
    print(pdf_file)
#    pdf_file = "pdfs/s_TM100B25.pdf"
    result = parse_model(pdf_file.stem)
    print(result)
    rows = parse_pdf(pdf_file)
    print(rows)

    conn = create_database(base_dir/"motors.db")
    insert_rows(conn,rows)
    convert_db_to_excel(base_dir/"motors.db")
"""
if __name__ == "__main__":

    base_dir = Path(__file__).parent

    db_file = base_dir / "motors.db"

    if db_file.exists():
        db_file.unlink()

    conn = create_database(db_file)

    import_folder(base_dir / "pdfs",conn)

    conn.close()

    convert_db_to_excel(db_file)