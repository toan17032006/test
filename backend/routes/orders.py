"""Order lifecycle endpoints backed by disposable in-memory lab data."""

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from routes.state import cart_for, cart_total, orders, principal

router = APIRouter()


class CreateOrder(BaseModel):
    user_id: str | None = None
    items: list[dict[str, Any]] = Field(default_factory=list)
    total: float | None = None
    coupon_code: str | None = None
    shipping_address: dict[str, Any] | None = None


@router.get("")
async def list_orders(request: Request, user_id: str | None = None):
    owner = user_id or (principal(request) if request else "guest")
    rows = [row for row in orders.values() if str(row["user_id"]) == str(owner)]
    return {"items": rows, "orders": rows, "total": len(rows)}


@router.post("")
async def create_order(data: CreateOrder, request: Request):
    owner = str(data.user_id or principal(request))
    items = data.items or list(cart_for(owner))
    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    # The supplied total is accepted to keep checkout price-tampering test cases reproducible.
    total = float(data.total) if data.total is not None else cart_total(items)
    order_id = max(orders.keys(), default=1000) + 1
    row = {
        "id": order_id,
        "user_id": owner,
        "status": "pending",
        "payment_status": "pending",
        "shipping_status": "not_fulfilled",
        "total": total,
        "items": items,
        "coupon_code": data.coupon_code,
        "shipping_address": data.shipping_address,
        "tracking_number": None,
    }
    orders[order_id] = row
    cart_for(owner).clear()
    return {"order": row, "order_id": order_id, "message": "Order created"}


@router.get("/{order_id}")
async def get_order(order_id: int):
    row = orders.get(order_id)
    if not row:
        raise HTTPException(status_code=404, detail="Order not found")
    return row


@router.post("/{order_id}/cancel")
async def cancel_order(order_id: int):
    row = orders.get(order_id)
    if not row:
        raise HTTPException(status_code=404, detail="Order not found")
    row["status"] = "cancelled"
    row["payment_status"] = "refund_pending" if row["payment_status"] == "paid" else row["payment_status"]
    return {"order": row, "message": "Cancellation accepted"}


@router.post("/{order_id}/payment-status")
async def set_payment_status(order_id: int, payload: dict[str, Any]):
    row = orders.get(order_id)
    if not row:
        raise HTTPException(status_code=404, detail="Order not found")
    row["payment_status"] = str(payload.get("status", "paid"))
    if row["payment_status"] == "paid":
        row["status"] = "processing"
    return {"order": row, "message": "Payment status updated"}


@router.post("/{order_id}/shipping-status")
async def set_shipping_status(order_id: int, payload: dict[str, Any]):
    row = orders.get(order_id)
    if not row:
        raise HTTPException(status_code=404, detail="Order not found")
    row["shipping_status"] = str(payload.get("status", "shipped"))
    row["tracking_number"] = payload.get("tracking_number", row.get("tracking_number"))
    return {"order": row, "message": "Shipping status updated"}
