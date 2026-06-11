import sqlite3
from pathlib import Path

DB_FILE = Path("app/database/motors.db")


def get_connection():
    return sqlite3.connect(DB_FILE)


def search_motors(
    target_speed: int,
    target_pull: int,
    limit: int = 20
):

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    query = """
    SELECT *
    FROM motor_performance

    ORDER BY
        ABS(speed_ftmin - ?) +
        ABS(belt_pull_lbf - ?)

    LIMIT ?
    """

    rows = conn.execute(
        query,
        (
            target_speed,
            target_pull,
            limit
        )
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_motor_by_id(motor_id: int):
    """Get a single motor record by ID"""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    
    query = """
    SELECT *
    FROM motor_performance
    WHERE id = ?
    """
    
    row = conn.execute(query, (motor_id,)).fetchone()
    conn.close()
    
    return dict(row) if row else None


def get_motor_specifications(motor_id: int):
    """
    Get motor specifications and split them into Metric and Imperial groups
    
    Returns:
        tuple: (metric_specs, imperial_specs) - each is a list of dicts with 'name', 'value', 'unit'
    """
    motor = get_motor_by_id(motor_id)
    
    if not motor:
        return [], []
    
    # Define specification mappings with their units
    # Format: (db_field, display_name, unit_type)
    spec_definitions = [
        # Metric specifications
        ('hp', 'Horsepower', 'metric'),
        ('drum_rpm', 'Drum RPM', 'metric'),
        ('stator_poles', 'Stator Poles', 'metric'),
        ('motor_model', 'Motor Model', 'metric'),
        ('gear_code', 'Gear Code', 'metric'),
        
        # Imperial specifications
        ('speed_ftmin', 'Speed', 'imperial'),  # ft/min
        ('belt_pull_lbf', 'Belt Pull', 'imperial'),  # lbf
    ]
    
    metric_specs = []
    imperial_specs = []
    
    for db_field, display_name, unit_type in spec_definitions:
        if db_field in motor and motor[db_field] is not None:
            spec_entry = {
                'name': display_name,
                'value': motor[db_field]
            }
            
            # Add appropriate unit
            if db_field == 'speed_ftmin':
                spec_entry['unit'] = 'ft/min'
            elif db_field == 'belt_pull_lbf':
                spec_entry['unit'] = 'lbf'
            elif db_field == 'hp':
                spec_entry['unit'] = 'HP'
            elif db_field == 'drum_rpm':
                spec_entry['unit'] = 'RPM'
            else:
                spec_entry['unit'] = ''
            
            if unit_type == 'metric':
                metric_specs.append(spec_entry)
            else:
                imperial_specs.append(spec_entry)
    
    return metric_specs, imperial_specs
