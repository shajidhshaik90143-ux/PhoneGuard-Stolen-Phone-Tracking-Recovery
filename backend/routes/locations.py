from fastapi import APIRouter, Depends, HTTPException

from backend.auth import get_current_user
from backend.database import get_connection
from backend.schemas import LocationCreate
from backend.services.location_service import (
    add_location,
    get_latest_location,
    get_location_history
)

router = APIRouter(
    prefix="/locations",
    tags=["Locations"]
)


def verify_device_owner(device_id: int, user_id: int):
    connection = get_connection()

    device = connection.execute(
        """
        SELECT *
        FROM devices
        WHERE id = ?
        AND user_id = ?
        """,
        (device_id, user_id)
    ).fetchone()

    connection.close()

    return device


@router.post("/{device_id}")
def update_location(
    device_id: int,
    data: LocationCreate,
    current_user=Depends(get_current_user)
):
    device = verify_device_owner(
        device_id,
        current_user["id"]
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    location_id = add_location(
        device_id=device_id,
        latitude=data.latitude,
        longitude=data.longitude,
        accuracy=data.accuracy,
        battery=data.battery,
        network_status=data.network_status
    )

    return {
        "message": "Location updated",
        "location_id": location_id
    }


@router.get("/{device_id}/latest")
def latest_location(
    device_id: int,
    current_user=Depends(get_current_user)
):
    device = verify_device_owner(
        device_id,
        current_user["id"]
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    location = get_latest_location(device_id)

    return {
        "device_id": device_id,
        "location": location
    }


@router.get("/{device_id}/history")
def location_history(
    device_id: int,
    current_user=Depends(get_current_user)
):
    device = verify_device_owner(
        device_id,
        current_user["id"]
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    return get_location_history(device_id)