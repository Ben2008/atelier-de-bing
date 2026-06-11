from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).parent
DB_NAME = BASE_DIR / "outline_drawing.db"

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

# ==========================================
# Main Drawing Table
# ==========================================

cur.execute("""
CREATE TABLE IF NOT EXISTS drawing_master (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    drawing_name TEXT UNIQUE,
    file_path TEXT,
    source_list TEXT,

    motor_type TEXT,
    material TEXT,

    drum_diameter INTEGER,
    flange_style TEXT,
    shaft_size INTEGER,

    brake_option TEXT,

    stator TEXT,
    speed REAL,
    hp REAL,
    gear_code TEXT,

    phase INTEGER,
    frequency INTEGER,
    voltage INTEGER,

    power_entry TEXT,

    face_width REAL,
    shell_profile TEXT,
    surface_finish TEXT,

    drawing_category TEXT,

    parse_status TEXT DEFAULT 'RAW'
)
""")

# ==========================================
# Lagging Table
# ==========================================

cur.execute("""
CREATE TABLE IF NOT EXISTS drawing_lagging (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    drawing_id INTEGER,

    lagging_material TEXT,
    lagging_thickness REAL,
    lagging_profile TEXT,

    FOREIGN KEY(drawing_id)
        REFERENCES drawing_master(id)
)
""")

# ==========================================
# Shaft Table
# ==========================================

cur.execute("""
CREATE TABLE IF NOT EXISTS drawing_shaft (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    drawing_id INTEGER,

    shaft_cross_section TEXT,
    shaft_x REAL,
    shaft_y REAL,

    FOREIGN KEY(drawing_id)
        REFERENCES drawing_master(id)
)
""")

# ==========================================
# Sprocket Table
# ==========================================

cur.execute("""
CREATE TABLE IF NOT EXISTS drawing_sprockets (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    drawing_id INTEGER,

    series TEXT,
    teeth INTEGER,
    material TEXT,
    quantity INTEGER,

    FOREIGN KEY(drawing_id)
        REFERENCES drawing_master(id)
)
""")

# ==========================================
# Drive Rod Table
# ==========================================

cur.execute("""
CREATE TABLE IF NOT EXISTS drawing_drive_rods (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    drawing_id INTEGER,

    rod_count INTEGER,
    series TEXT,

    FOREIGN KEY(drawing_id)
        REFERENCES drawing_master(id)
)
""")

# ==========================================
# Feature Table
# ==========================================

cur.execute("""
CREATE TABLE IF NOT EXISTS drawing_features (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    drawing_id INTEGER,

    feature_code TEXT,
    feature_value TEXT,

    FOREIGN KEY(drawing_id)
        REFERENCES drawing_master(id)
)
""")

# ==========================================
# Token Dictionary
# ==========================================

cur.execute("""
CREATE TABLE IF NOT EXISTS token_dictionary (

    token TEXT PRIMARY KEY,

    description TEXT,
    category TEXT,
    active INTEGER DEFAULT 1
)
""")

conn.commit()
conn.close()

print(f"Database created successfully:")
print(DB_NAME)