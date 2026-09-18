from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from backend.auth import get_current_user
from backend.database import get_connection
from backend.services.location_service import get_latest_location
from backend.services.report_service import generate_theft_report

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

REPORT_DIR = (
    Path(__file__).resolve().parent.parent.parent
    / "reports"
)

REPORT_DIR.mkdir(exist_ok=True)


@router.get("/{device_id}/theft-report")
def theft_report(
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

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (current_user["id"],)
    ).fetchone()

    connection.close()

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    latest_location = get_latest_location(device_id)

    output_file = REPORT_DIR / (
        f"phoneguard_report_{device_id}.pdf"
    )

    generate_theft_report(
        owner_name=user["name"],
        owner_email=user["email"],
        device=dict(device),
        latest_location=latest_location,
        output_path=output_file
    )

    return FileResponse(
        path=output_file,
        media_type="application/pdf",
        filename=output_file.name
    )