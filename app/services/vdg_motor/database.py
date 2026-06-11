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
    
    # Try to use pre-calculated values from database first
    if 'cal_Vs' in motor and motor['cal_Vs'] is not None:
        derived['Vs'] = motor['cal_Vs']
    else:
        # Calculate Synchronous velocity: Vs = Hz * 60 * 2 / Poles
        if 'frequency_hz' in motor and motor['frequency_hz'] is not None and \
           'stator_poles' in motor and motor['stator_poles'] is not None:
            frequency = motor['frequency_hz']
            poles = motor['stator_poles']
            if poles > 0:
                vs = frequency * 60 * 2 / poles
                derived['Vs'] = vs
    
    # Try to use pre-calculated Vr from database
    if 'cal_Vr' in motor and motor['cal_Vr'] is not None:
        derived['Vr'] = motor['cal_Vr']
    else:
        # Calculate Actual rotor speed: Vr = Vs * (1 - slip)
        if 'Vs' in derived or ('cal_Vs' in motor and motor['cal_Vs'] is not None):
            vs = derived.get('Vs', motor.get('cal_Vs'))
            if vs:
                slip = DEFAULT_SLIP  # 2%
                vr = vs * (1 - slip)
                derived['Vr'] = round(vr, 0)  # Round to integer
    
    # Try to use pre-calculated Gear Ratio from database
    if 'cal_Gear_ratio' in motor and motor['cal_Gear_ratio'] is not None:
        derived['Gear_ratio'] = motor['cal_Gear_ratio']
    else:
        # Calculate Gear ratio: Gear_ratio = Vr / RPM
        vr = derived.get('Vr')
        if not vr and 'cal_Vr' in motor:
            vr = motor['cal_Vr']
        
        if vr:
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
    Get motor specifications and format for display
    
    Returns:
        tuple: (conversion_specs) - formatted for display
    """
    motor = get_motor_by_id(motor_id)
    
    if not motor:
        return []
    
    conversion_specs = []
    
    # Power conversion: kW to HP
    power_kw = motor.get('cal_Power_kW')
    if not power_kw and motor.get('hp'):
        power_kw = round(motor['hp'] * 0.746, 3)
    
    if power_kw and motor.get('hp'):
        conversion_specs.append({
            'name': 'Power',
            'metric_value': power_kw,
            'metric_unit': 'kW',
            'imperial_value': motor['hp'],
            'imperial_unit': 'HP'
        })
    
    # Speed conversion: m/s to ft/min
    speed_ms = motor.get('cal_Speed_ms')
    if not speed_ms and motor.get('speed_ftmin'):
        speed_ms = round(motor['speed_ftmin'] * 0.00508, 3)
    
    if speed_ms and motor.get('speed_ftmin'):
        conversion_specs.append({
            'name': 'Speed',
            'metric_value': speed_ms,
            'metric_unit': 'm/s',
            'imperial_value': motor['speed_ftmin'],
            'imperial_unit': 'ft/min'
        })
    
    # Belt pull conversion: N to lbf
    belt_pull_n = motor.get('cal_Belt_pull_N')
    if not belt_pull_n and motor.get('belt_pull_lbf'):
        belt_pull_n = round(motor['belt_pull_lbf'] * 4.448, 3)
    
    if belt_pull_n and motor.get('belt_pull_lbf'):
        conversion_specs.append({
            'name': 'Belt Pull',
            'metric_value': belt_pull_n,
            'metric_unit': 'N',
            'imperial_value': motor['belt_pull_lbf'],
            'imperial_unit': 'lbf'
        })
    
    return conversion_specs
