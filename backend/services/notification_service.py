def create_security_message(
    device_name: str,
    status: str,
    latitude=None,
    longitude=None
):
    if latitude is not None and longitude is not None:
        location_text = (
            f"Location: {latitude}, {longitude}"
        )
    else:
        location_text = "Location unavailable"

    return (
        f"PhoneGuard Security Alert\n"
        f"Device: {device_name}\n"
        f"Status: {status}\n"
        f"{location_text}"
    )