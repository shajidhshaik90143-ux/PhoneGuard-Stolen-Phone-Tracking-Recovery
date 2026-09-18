# PhoneGuard

PhoneGuard is an authorized lost and stolen phone management system.

## Features

- User registration
- User authentication
- Device registration
- IMEI/device identification records
- Phone number records
- GPS location updates
- Last known location
- Location history
- Lost/Stolen status
- Streamlit dashboard
- PDF security report
- SQLite database
- FastAPI backend

## Architecture

Android Phone
       |
       v
Authorized GPS Location
       |
       v
FastAPI Backend
       |
       v
SQLite Database
       |
       v
Streamlit Dashboard

## Run Backend

```bash
uvicorn backend.main:app --reload