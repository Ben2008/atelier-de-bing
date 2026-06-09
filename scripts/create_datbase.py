import sqlite3

conn = sqlite3.connect("motors.db")

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS motor_performance (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    motor_model TEXT,

    shell_od_mm INTEGER,
    shaft_type TEXT,
    shaft_od_mm INTEGER,

    hp REAL,

    speed_ftmin INTEGER,
    belt_pull_lbf INTEGER,
    drum_rpm INTEGER,

    stator_poles INTEGER,
    gear_code TEXT,

    source_pdf TEXT
)
""")

conn.commit()