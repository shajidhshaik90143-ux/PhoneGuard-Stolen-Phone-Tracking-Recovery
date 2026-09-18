from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_theft_report(
    owner_name,
    owner_email,
    device,
    latest_location,
    output_path
):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pdf = canvas.Canvas(
        str(output_path),
        pagesize=A4
    )

    width, height = A4

    y = height - 60

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(
        50,
        y,
        "PhoneGuard - Device Security Report"
    )

    y -= 50

    pdf.setFont("Helvetica", 11)

    information = [
        ("Owner Name", owner_name),
        ("Owner Email", owner_email),
        ("Device Name", device["device_name"]),
        ("IMEI", device["imei"]),
        ("Phone Number", device["phone_number"]),
        ("Model", device["model"] or "Not provided"),
        ("Status", device["status"]),
    ]

    for label, value in information:
        pdf.drawString(
            60,
            y,
            f"{label}: {value}"
        )
        y -= 25

    y -= 10

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(
        60,
        y,
        "Last Known Location"
    )

    y -= 30

    pdf.setFont("Helvetica", 11)

    if latest_location:
        location_data = [
            f"Latitude: {latest_location['latitude']}",
            f"Longitude: {latest_location['longitude']}",
            f"Accuracy: {latest_location['accuracy']}",
            f"Battery: {latest_location['battery']}",
            f"Network: {latest_location['network_status']}",
            f"Recorded At: {latest_location['recorded_at']}",
        ]

        for item in location_data:
            pdf.drawString(60, y, item)
            y -= 25

    else:
        pdf.drawString(
            60,
            y,
            "No location has been reported."
        )

    y -= 30

    pdf.setFont("Helvetica-Oblique", 9)
    pdf.drawString(
        60,
        y,
        "This report contains information supplied by the registered device."
    )

    pdf.save()

    return str(output_path)