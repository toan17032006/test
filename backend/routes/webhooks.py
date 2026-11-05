"""Local webhook handlers. No callback URL is fetched and no real provider is contacted."""

from typing import Any

from fastapi import APIRouter, Request

from routes.state import orders

router = APIRouter()
received_events: list[dict[str, Any]] = []


@router.post("/payment")
async def payment_webhook(request: Request):
    payload = await request.json()
    received_events.append(payload)
    order_id = payload.get("order_id")
    order = orders.get(int(order_id)) if order_id is not None and str(order_id).isdigit() else None
    if order:
        order["payment_status"] = str(payload.get("status", "paid"))
        if order["payment_status"] == "paid":
            order["status"] = "processing"
    return {"accepted": True, "duplicate_count": sum(event == payload for event in received_events), "order": order}


@router.post("/shipping")
async def shipping_webhook(request: Request):
    payload = await request.json()
    order_id = payload.get("order_id")
    order = orders.get(int(order_id)) if order_id is not None and str(order_id).isdigit() else None
    if order:
        order["shipping_status"] = str(payload.get("status", "shipped"))
        order["tracking_number"] = payload.get("tracking_number", order.get("tracking_number"))
    return {"accepted": True, "order": order}


@router.post("/inventory")
async def inventory_webhook(payload: dict[str, Any]):
    return {"accepted": True, "product_id": payload.get("product_id"), "quantity": payload.get("quantity"), "action": payload.get("action", "adjust")}
