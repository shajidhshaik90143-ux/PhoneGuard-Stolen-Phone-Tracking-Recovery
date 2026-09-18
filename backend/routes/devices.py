from fastapi import APIRouter, Depends, HTTPException

from backend.auth import get_current_user
from backend.database import get_connection
from backend.schemas import DeviceCreate, StatusUpdate

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


@router.post("/")
def create_device(
    data: DeviceCreate,
    current_user=Depends(get_current_user)
):
    connection = get_connection()

    existing = connection.execute(
        """
        SELECT id
        FROM devices
        WHERE imei = ?
        """,
        (data.imei,)
    ).fetchone()

    if existing:
        connection.close()

        raise HTTPException(
            status_code=409,
            detail="This IMEI is already registered"
        )

    cursor = connection.execute(
        """
        INSERT INTO devices
        (
            user_id,
            device_name,
            imei,
            phone_number,
            model
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            current_user["id"],
            data.device_name,
            data.imei,
            data.phone_number,
            data.model
        )
    )

    device_id = cursor.lastrowid

    connection.commit()

    device = connection.execute(
        """
        SELECT *
        FROM devices
        WHERE id = ?
        """,
        (device_id,)
    ).fetchone()

    connection.close()

    return dict(device)


@router.get("/")
def get_devices(
    current_user=Depends(get_current_user)
):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM devices
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (current_user["id"],)
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


@router.get("/{device_id}")
def get_device(
    device_id: int,
    current_user=Depends(get_current_user)
):
    connection = get_connection()

    device = connection.execute(
        """
        SELECT *
        FROM devices
        WHERE id = ?
        AND user_id = ?
        """,
        (device_id, current_user["id"])
    ).fetchone()

    connection.close()

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    return dict(device)


@router.patch("/{device_id}/status")
def update_status(
    device_id: int,
    data: StatusUpdate,
    current_user=Depends(get_current_user)
):
    allowed_statuses = {
        "NORMAL",
        "LOST",
        "STOLEN",
        "RECOVERED"
    }

    status = data.status.upper()

    if status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid device status"
        )

    connection = get_connection()

    device = connection.execute(
        """
        SELECT id
        FROM devices
        WHERE id = ?
        AND user_id = ?
        """,
        (device_id, current_user["id"])
    ).fetchone()

    if not device:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    connection.execute(
        """
        UPDATE devices
        SET status = ?
        WHERE id = ?
        """,
        (status, device_id)
    )

    connection.commit()
    connection.close()

    return {
        "message": "Device status updated",
        "status": status
    }