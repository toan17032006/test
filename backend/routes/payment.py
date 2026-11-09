"""Mock payment endpoints; no real provider or money movement is used."""

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from routes.state import orders, payments

router = APIRouter()


class PaymentRequest(BaseModel):
    order_id: int
    amount: float | None = None
    currency: str = "VND"
    method: str = "card"


@router.post("/intent")
async def create_intent(data: PaymentRequest):
    order = orders.get(data.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    amount = float(data.amount if data.amount is not None else order["total"])
    payment_id = f"pay_{data.order_id}_{len(payments.get(data.order_id, [])) + 1}"
    payment = {"id": payment_id, "order_id": data.order_id, "amount": amount, "currency": data.currency, "method": data.method, "status": "pending"}
    payments.setdefault(data.order_id, []).append(payment)
    return {"payment": payment, "client_secret": f"{payment_id}_secret_lab"}


@router.post("/process")
async def process_payment(data: PaymentRequest):
    order = orders.get(data.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    amount = float(data.amount if data.amount is not None else order["total"])
    payment = {"id": f"pay_{data.order_id}_{len(payments.get(data.order_id, [])) + 1}", "order_id": data.order_id, "amount": amount, "currency": data.currency, "method": data.method, "status": "succeeded"}
    payments.setdefault(data.order_id, []).append(payment)
    order["payment_status"] = "paid"
    order["status"] = "processing"
    return {"payment": payment, "order": order}


@router.get("/{order_id}")
async def payment_history(order_id: int):
    return {"order_id": order_id, "payments": payments.get(order_id, [])}


@router.post("/{order_id}/refund")
async def refund_payment(order_id: int, payload: dict[str, Any]):
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    refund = {"order_id": order_id, "amount": payload.get("amount", order["total"]), "status": "refunded"}
    order["payment_status"] = "refunded"
    return refund
