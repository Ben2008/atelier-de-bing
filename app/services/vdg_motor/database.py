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