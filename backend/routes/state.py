"""In-memory state shared by the e-commerce API routers."""

from typing import Any


carts: dict[str, list[dict[str, Any]]] = {}
orders: dict[int, dict[str, Any]] = {
    1001: {
        "id": 1001,
        "user_id": "2",
        "status": "delivered",
        "payment_status": "paid",
        "shipping_status": "delivered",
        "total": 29990000,
        "items": [{"product_id": 1, "name": "iPhone 15 Pro Max", "quantity": 1, "unit_price": 29990000}],
        "tracking_number": "VN-LAB-1001",
    },
    1002: {
        "id": 1002,
        "user_id": "3",
        "status": "processing",
        "payment_status": "pending",
        "shipping_status": "preparing",
        "total": 2890000,
        "items": [{"product_id": 5, "name": "Nike Air Force 1", "quantity": 1, "unit_price": 2890000}],
        "tracking_number": None,
    },
}
payments: dict[int, list[dict[str, Any]]] = {}
notifications: list[dict[str, Any]] = []
uploaded_files: dict[str, dict[str, Any]] = {}


def principal(request) -> str:
    """Resolve a demo principal from request metadata (lab-only identity)."""
    return str(
        request.headers.get("x-user-id")
        or request.query_params.get("user_id")
        or request.cookies.get("user_id")
        or "guest"
    )


def cart_for(user_id: str) -> list[dict[str, Any]]:
    return carts.setdefault(user_id, [])


def cart_total(items: list[dict[str, Any]]) -> float:
    return sum(float(item.get("unit_price", 0)) * int(item.get("quantity", 0)) for item in items)
