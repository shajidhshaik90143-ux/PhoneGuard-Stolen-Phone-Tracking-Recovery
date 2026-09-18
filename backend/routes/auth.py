from fastapi import APIRouter, HTTPException

from backend.auth import (
    create_access_token,
    hash_password,
    verify_password
)
from backend.database import get_connection
from backend.schemas import LoginRequest, RegisterRequest

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(data: RegisterRequest):
    connection = get_connection()

    existing = connection.execute(
        "SELECT id FROM users WHERE email = ?",
        (data.email.lower().strip(),)
    ).fetchone()

    if existing:
        connection.close()

        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    cursor = connection.execute(
        """
        INSERT INTO users
        (
            name,
            email,
            password_hash
        )
        VALUES (?, ?, ?)
        """,
        (
            data.name.strip(),
            data.email.lower().strip(),
            hash_password(data.password)
        )
    )

    user_id = cursor.lastrowid

    connection.commit()
    connection.close()

    token = create_access_token(
        user_id,
        data.email.lower().strip()
    )

    return {
        "message": "Registration successful",
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/login")
def login(data: LoginRequest):
    connection = get_connection()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (data.email.lower().strip(),)
    ).fetchone()

    connection.close()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        data.password,
        user["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        user["id"],
        user["email"]
    )

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }