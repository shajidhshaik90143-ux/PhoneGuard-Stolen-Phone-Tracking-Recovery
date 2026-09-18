from backend.database import get_connection


def add_location(
    device_id: int,
    latitude: float,
    longitude: float,
    accuracy=None,
    battery=None,
    network_status=None
):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO locations
        (
            device_id,
            latitude,
            longitude,
            accuracy,
            battery,
            network_status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            device_id,
            latitude,
            longitude,
            accuracy,
            battery,
            network_status
        )
    )

    location_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return location_id


def get_latest_location(device_id: int):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM locations
        WHERE device_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (device_id,)
    ).fetchone()

    connection.close()

    return dict(row) if row else None


def get_location_history(device_id: int, limit: int = 100):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM locations
        WHERE device_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (device_id, limit)
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]