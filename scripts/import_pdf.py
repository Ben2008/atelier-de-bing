from pathlib import Path

pdf_folder = Path("pdfs")

for pdf_file in pdf_folder.glob("*.pdf"):

    try:

        rows = parse_pdf(pdf_file)

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

            ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,?
            )
            """, (

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

        print(f"Imported {pdf_file}")

    except Exception as ex:

        print(f"FAILED: {pdf_file}")
        print(ex)

conn.commit()
conn.close()