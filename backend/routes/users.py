"""Customer profile and address endpoints using the auth demo store."""

from fastapi import APIRouter, HTTPException

from routes.auth import users_db

router = APIRouter()


def user_rows():
    return list(users_db.values())


@router.get("")
async def list_users():
    return {"items": user_rows(), "total": len(users_db)}


@router.get("/{user_id}/addresses")
async def addresses(user_id: int):
    user = next((row for row in users_db.values() if int(row["id"]) == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "addresses": [{"id": 1, "label": "Default", "address": user.get("address", ""), "phone": user.get("phone", "")}]}


@router.get("/{user_id}")
async def get_user(user_id: int):
    user = next((row for row in users_db.values() if int(row["id"]) == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}")
async def update_user(user_id: int, payload: dict):
    user = next((row for row in users_db.values() if int(row["id"]) == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.update(payload)
    return {"user": user, "message": "Profile updated"}
