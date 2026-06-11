import sqlite3
from pathlib import Path

DB_FILE = Path("app/database/motors.db")

# Default slip percentage (2%)
DEFAULT_SLIP = 0.02


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


def calculate_derived_specs(motor: dict) -> dict:
    """
    Calculate derived specifications from base parameters
    
    Formulas:
    - Vsynchronous = Frequency(Hz) * 60 * 2 / Poles
    - Slip = 2% (default)
    - Vr = Vs * (1 - slip), rounded to 0 digits (integer)
    - Gear ratio = Vr / RPM (or cal_RPM if available)
    
    Unit conversions (use cal_ prefix values if available):
    - cal_Power_kW = Power(HP) * 0.746
    - cal_Speed_ms = Speed(ft/min) * 0.00508
    - cal_Belt_pull_N = Belt_pull(lbf) * 4.448
    """
    derived = {}
    
    # Synchronous velocity: Vs = Hz * 60 * 2 / Poles
    if 'frequency_hz' in motor and motor['frequency_hz'] is not None and \
       'stator_poles' in motor and motor['stator_poles'] is not None:
        frequency = motor['frequency_hz']
        poles = motor['stator_poles']
        if poles > 0:
            vs = frequency * 60 * 2 / poles
            derived['Vs'] = vs
            
            # Actual rotor speed: Vr = Vs * (1 - slip)
            slip = DEFAULT_SLIP  # 2%
            vr = vs * (1 - slip)
            derived['Vr'] = round(vr, 0)  # Round to integer
            
            # Gear ratio: Gear_ratio = Vr / RPM
            # Use cal_RPM if available, otherwise use drum_rpm
            rpm = motor.get('cal_RPM', motor.get('drum_rpm'))
            if rpm and rpm > 0:
                gear_ratio = vr / rpm
                derived['Gear_ratio'] = round(gear_ratio, 3)
    
    # Power conversion (HP to kW) - use cal_Power_kW if available
    if 'cal_Power_kW' in motor and motor['cal_Power_kW'] is not None:
        derived['Power_kW'] = motor['cal_Power_kW']
    elif 'hp' in motor and motor['hp'] is not None:
        derived['Power_kW'] = round(motor['hp'] * 0.746, 3)
    
    # Speed conversion (ft/min to m/s) - use cal_Speed_ms if available
    if 'cal_Speed_ms' in motor and motor['cal_Speed_ms'] is not None:
        derived['Speed_ms'] = motor['cal_Speed_ms']
    elif 'speed_ftmin' in motor and motor['speed_ftmin'] is not None:
        derived['Speed_ms'] = round(motor['speed_ftmin'] * 0.00508, 3)
    
    # Belt pull conversion (lbf to N) - use cal_Belt_pull_N if available
    if 'cal_Belt_pull_N' in motor and motor['cal_Belt_pull_N'] is not None:
        derived['Belt_pull_N'] = motor['cal_Belt_pull_N']
    elif 'belt_pull_lbf' in motor and motor['belt_pull_lbf'] is not None:
        derived['Belt_pull_N'] = round(motor['belt_pull_lbf'] * 4.448, 3)
    
    # Surface velocity (if shell_od_mm available)
    if 'cal_RPM' in motor and motor['cal_RPM'] is not None and \
       'shell_od_mm' in motor and motor['shell_od_mm'] is not None:
        rpm = motor['cal_RPM']
        shell_od = motor['shell_od_mm']
        surface_velocity = rpm * shell_od / 60000
        derived['Surface_velocity_ms'] = round(surface_velocity, 3)
    elif 'drum_rpm' in motor and motor['drum_rpm'] is not None and \
         'shell_od_mm' in motor and motor['shell_od_mm'] is not None:
        rpm = motor['drum_rpm']
        shell_od = motor['shell_od_mm']
        surface_velocity = rpm * shell_od / 60000
        derived['Surface_velocity_ms'] = round(surface_velocity, 3)
    
    return derived


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
        ('drum_rpm', 'Drum RPM', 'metric'),
        ('stator_poles', 'Stator Poles', 'metric'),
        ('frequency_hz', 'Frequency', 'metric'),  # Hz
        
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
            elif db_field == 'drum_rpm':
                spec_entry['unit'] = 'RPM'
            elif db_field == 'stator_poles':
                spec_entry['unit'] = ''
            elif db_field == 'frequency_hz':
                spec_entry['unit'] = 'Hz'
            else:
                spec_entry['unit'] = ''
            
            if unit_type == 'metric':
                metric_specs.append(spec_entry)
            else:
                imperial_specs.append(spec_entry)
    
    return metric_specs, imperial_specs
