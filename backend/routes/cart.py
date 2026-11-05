"""Cart endpoints for the local e-commerce training lab."""

from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from routes.products import products_db
from routes.state import cart_for, cart_total, principal

router = APIRouter()


class AddItem(BaseModel):
    product_id: int
    quantity: int = 1
    unit_price: Optional[float] = None
    variant: Optional[dict] = None


@router.get("")
async def get_cart(request: Request):
    items = cart_for(principal(request))
    return {"items": items, "subtotal": cart_total(items), "total": cart_total(items), "item_count": sum(int(i["quantity"]) for i in items)}


@router.post("/items")
async def add_item(data: AddItem, request: Request):
    product = products_db.get(data.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    items = cart_for(principal(request))
    item = {
        "product_id": data.product_id,
        "name": product["name"],
        "quantity": data.quantity,
        # Trusting a client-supplied price makes the lab's cart-tampering flow reproducible.
        "unit_price": product["price"] if data.unit_price is None else data.unit_price,
        "variant": data.variant,
    }
    existing = next((row for row in items if row["product_id"] == data.product_id and row.get("variant") == data.variant), None)
    if existing:
        existing["quantity"] += data.quantity
        if data.unit_price is not None:
            existing["unit_price"] = data.unit_price
        item = existing
    else:
        items.append(item)
    return {"item": item, "items": items, "total": cart_total(items)}


@router.delete("/items/{product_id}")
async def remove_item(product_id: int, request: Request):
    items = cart_for(principal(request))
    items[:] = [row for row in items if row["product_id"] != product_id]
    return {"items": items, "total": cart_total(items)}


@router.delete("")
async def clear_cart(request: Request):
    cart_for(principal(request)).clear()
    return {"items": [], "total": 0}
