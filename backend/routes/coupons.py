"""Coupon examples for checkout workflow testing."""

from fastapi import APIRouter

router = APIRouter()
COUPONS = {
    "SALE10": {"type": "percent", "discount": 10},
    "FLAT50K": {"type": "fixed", "discount": 50000},
    "VIP": {"type": "percent", "discount": 50},
    "ADMIN": {"type": "percent", "discount": 100},
}


@router.post("/validate")
async def validate_coupon(payload: dict):
    code = str(payload.get("code", "")).upper()
    coupon = COUPONS.get(code)
    total = float(payload.get("total", 0) or 0)
    discount_amount = 0
    if coupon:
        discount_amount = total * coupon["discount"] / 100 if coupon["type"] == "percent" else coupon["discount"]
    return {"valid": coupon is not None, "code": code if coupon else None, "discount": coupon, "discount_amount": discount_amount, "total_after_discount": max(0, total-discount_amount)}


@router.get("")
async def list_coupons():
    return {"items": [{"code": code, **data} for code, data in COUPONS.items()]}
