from typing import Optional

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str
    password: str = Field(min_length=6, max_length=100)


class LoginRequest(BaseModel):
    email: str
    password: str


class DeviceCreate(BaseModel):
    device_name: str = Field(min_length=1, max_length=100)
    imei: str = Field(min_length=5, max_length=30)
    phone_number: str = Field(min_length=5, max_length=30)
    model: Optional[str] = Field(default=None, max_length=100)


class LocationCreate(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    accuracy: Optional[float] = Field(default=None, ge=0)
    battery: Optional[float] = Field(default=None, ge=0, le=100)
    network_status: Optional[str] = Field(default=None, max_length=50)


class StatusUpdate(BaseModel):
    status: str