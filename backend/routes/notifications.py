"""In-memory notification feed for the lab storefront."""

from typing import Any

from fastapi import APIRouter, Request

from routes.state import notifications, principal

router = APIRouter()


@router.get("")
async def list_notifications(request: Request):
    user_id = principal(request)
    rows = [row for row in notifications if row["user_id"] == user_id]
    return {"items": rows, "unread": sum(not row["read"] for row in rows)}


@router.post("")
async def create_notification(payload: dict[str, Any]):
    row = {"id": len(notifications) + 1, "user_id": str(payload.get("user_id", "guest")), "title": str(payload.get("title", "Thông báo")), "message": str(payload.get("message", "")), "read": False}
    notifications.append(row)
    return {"notification": row}


@router.post("/{notification_id}/read")
async def mark_read(notification_id: int):
    row = next((item for item in notifications if item["id"] == notification_id), None)
    if not row:
        return {"updated": False}
    row["read"] = True
    return {"updated": True, "notification": row}
