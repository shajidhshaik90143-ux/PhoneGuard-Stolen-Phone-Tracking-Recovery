from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: int
    name: str
    email: str


@dataclass
class Device:
    id: int
    user_id: int
    device_name: str
    imei: str
    phone_number: str
    model: Optional[str]
    status: str


@dataclass
class Location:
    id: int
    device_id: int
    latitude: float
    longitude: float
    accuracy: Optional[float]
    battery: Optional[float]
    network_status: Optional[str]
    recorded_at: str