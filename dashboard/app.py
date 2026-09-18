import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="PhoneGuard",
    page_icon="📱",
    layout="wide"
)

st.title("📱 PhoneGuard")
st.caption(
    "Lost & Stolen Phone Security Dashboard"
)


if "token" not in st.session_state:
    st.session_state.token = None

if "user_email" not in st.session_state:
    st.session_state.user_email = ""


def api_headers():
    return {
        "Authorization": (
            f"Bearer {st.session_state.token}"
        )
    }


menu = st.sidebar.selectbox(
    "Menu",
    [
        "Login",
        "Register",
        "Dashboard",
        "Devices",
        "Location",
        "Location History",
        "Reports"
    ]
)


if menu == "Register":

    st.header("Create Account")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Register"):

        try:
            response = requests.post(
                f"{API_URL}/auth/register",
                json={
                    "name": name,
                    "email": email,
                    "password": password
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()

                st.success(
                    "Registration successful. "
                    "You can now login."
                )

            else:
                st.error(
                    response.json().get(
                        "detail",
                        "Registration failed"
                    )
                )

        except requests.RequestException as error:
            st.error(f"API connection error: {error}")


elif menu == "Login":

    st.header("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        try:
            response = requests.post(
                f"{API_URL}/auth/login",
                json={
                    "email": email,
                    "password": password
                },
                timeout=10
            )

            if response.status_code == 200:

                data = response.json()

                st.session_state.token = (
                    data["access_token"]
                )

                st.session_state.user_email = email

                st.success("Login successful!")

                st.rerun()

            else:
                st.error(
                    response.json().get(
                        "detail",
                        "Login failed"
                    )
                )

        except requests.RequestException as error:
            st.error(f"API connection error: {error}")


elif menu == "Dashboard":

    st.header("📊 PhoneGuard Dashboard")

    if not st.session_state.token:
        st.warning("Please login first.")
        st.stop()

    try:
        response = requests.get(
            f"{API_URL}/devices/",
            headers=api_headers(),
            timeout=10
        )

        if response.status_code != 200:
            st.error("Unable to load devices.")
            st.stop()

        devices = response.json()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Registered Devices",
            len(devices)
        )

        stolen = sum(
            1
            for device in devices
            if device["status"] == "STOLEN"
        )

        lost = sum(
            1
            for device in devices
            if device["status"] == "LOST"
        )

        col2.metric(
            "Lost / Stolen",
            lost + stolen
        )

        col3.metric(
            "Normal",
            sum(
                1
                for device in devices
                if device["status"] == "NORMAL"
            )
        )

        st.subheader("Registered Devices")

        for device in devices:

            with st.container(border=True):

                st.write(
                    f"### 📱 {device['device_name']}"
                )

                st.write(
                    f"Model: {device['model'] or 'Unknown'}"
                )

                st.write(
                    f"Phone: {device['phone_number']}"
                )

                st.write(
                    f"Status: **{device['status']}**"
                )

    except requests.RequestException as error:
        st.error(f"API connection error: {error}")


elif menu == "Devices":

    st.header("📱 Device Management")

    if not st.session_state.token:
        st.warning("Please login first.")
        st.stop()

    st.subheader("Register Device")

    device_name = st.text_input(
        "Device Name",
        placeholder="My Android Phone"
    )

    imei = st.text_input(
        "IMEI",
        placeholder="Enter your own device IMEI"
    )

    phone_number = st.text_input(
        "Phone Number"
    )

    model = st.text_input(
        "Phone Model"
    )

    if st.button("Register Device"):

        try:
            response = requests.post(
                f"{API_URL}/devices/",
                headers=api_headers(),
                json={
                    "device_name": device_name,
                    "imei": imei,
                    "phone_number": phone_number,
                    "model": model
                },
                timeout=10
            )

            if response.status_code == 200:
                st.success(
                    "Device registered successfully."
                )
                st.json(response.json())

            else:
                st.error(
                    response.json().get(
                        "detail",
                        "Device registration failed"
                    )
                )

        except requests.RequestException as error:
            st.error(f"API connection error: {error}")

    st.divider()

    st.subheader("Your Devices")

    response = requests.get(
        f"{API_URL}/devices/",
        headers=api_headers()
    )

    if response.status_code == 200:

        devices = response.json()

        for device in devices:

            st.write(
                f"**{device['device_name']}** — "
                f"{device['status']}"
            )

            st.caption(
                f"IMEI: {device['imei']} | "
                f"Phone: {device['phone_number']}"
            )


elif menu == "Location":

    st.header("📍 Device Location")

    if not st.session_state.token:
        st.warning("Please login first.")
        st.stop()

    response = requests.get(
        f"{API_URL}/devices/",
        headers=api_headers()
    )

    if response.status_code != 200:
        st.error("Unable to load devices.")
        st.stop()

    devices = response.json()

    if not devices:
        st.info("Register a device first.")
        st.stop()

    device_options = {
        f"{d['device_name']} ({d['status']})": d["id"]
        for d in devices
    }

    selected = st.selectbox(
        "Select Device",
        list(device_options.keys())
    )

    device_id = device_options[selected]

    response = requests.get(
        f"{API_URL}/locations/{device_id}/latest",
        headers=api_headers()
    )

    if response.status_code == 200:

        data = response.json()
        location = data.get("location")

        if location:

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Latitude",
                location["latitude"]
            )

            col2.metric(
                "Longitude",
                location["longitude"]
            )

            col3.metric(
                "Battery",
                (
                    f"{location['battery']}%"
                    if location["battery"] is not None
                    else "Unknown"
                )
            )

            from dashboard.utils.maps import (
                display_location_map
            )

            display_location_map(
                location["latitude"],
                location["longitude"]
            )

            st.write(
                f"Last updated: "
                f"{location['recorded_at']}"
            )

        else:
            st.info(
                "No location has been received "
                "from this device yet."
            )

    else:
        st.error("Unable to retrieve location.")


elif menu == "Location History":

    st.header("🕒 Location History")

    if not st.session_state.token:
        st.warning("Please login first.")
        st.stop()

    response = requests.get(
        f"{API_URL}/devices/",
        headers=api_headers()
    )

    if response.status_code != 200:
        st.error("Unable to load devices.")
        st.stop()

    devices = response.json()

    if not devices:
        st.info("Register a device first.")
        st.stop()

    options = {
        d["device_name"]: d["id"]
        for d in devices
    }

    selected = st.selectbox(
        "Device",
        list(options.keys())
    )

    device_id = options[selected]

    response = requests.get(
        f"{API_URL}/locations/{device_id}/history",
        headers=api_headers()
    )

    if response.status_code == 200:

        history = response.json()

        if history:

            for item in history:

                with st.container(border=True):

                    st.write(
                        f"📍 "
                        f"{item['latitude']}, "
                        f"{item['longitude']}"
                    )

                    st.write(
                        f"Time: {item['recorded_at']}"
                    )

                    st.write(
                        f"Accuracy: "
                        f"{item['accuracy']}"
                    )

                    st.write(
                        f"Battery: "
                        f"{item['battery']}%"
                    )

        else:
            st.info(
                "No location history available."
            )


elif menu == "Reports":

    st.header("📄 Security Reports")

    if not st.session_state.token:
        st.warning("Please login first.")
        st.stop()

    response = requests.get(
        f"{API_URL}/devices/",
        headers=api_headers()
    )

    if response.status_code != 200:
        st.error("Unable to load devices.")
        st.stop()

    devices = response.json()

    if not devices:
        st.info("Register a device first.")
        st.stop()

    options = {
        d["device_name"]: d["id"]
        for d in devices
    }

    selected = st.selectbox(
        "Select Device",
        list(options.keys())
    )

    device_id = options[selected]

    if st.button("Generate Theft Report"):

        response = requests.get(
            f"{API_URL}/reports/"
            f"{device_id}/theft-report",
            headers=api_headers()
        )

        if response.status_code == 200:

            st.download_button(
                label="📥 Download PDF Report",
                data=response.content,
                file_name=(
                    f"phoneguard_report_{device_id}.pdf"
                ),
                mime="application/pdf"
            )

            st.success(
                "Report generated successfully."
            )

        else:
            st.error(
                "Unable to generate report."
            )