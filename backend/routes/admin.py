"""Admin management endpoints for the disposable pentest lab."""

from fastapi import APIRouter, HTTPException

from config import ADMIN_EMAIL, ADMIN_PASSWORD, DATABASE_URL, JWT_SECRET
from routes.auth import users_db
from routes.products import products_db
from routes.state import orders

router = APIRouter()


@router.get("/overview")
async def overview():
    return {"users": len(users_db), "products": len(products_db), "orders": len(orders), "pending_orders": sum(row["status"] == "pending" for row in orders.values())}


@router.get("/users")
async def admin_users():
    return {"items": list(users_db.values()), "total": len(users_db)}


@router.patch("/users/{user_id}/role")
async def change_role(user_id: int, payload: dict):
    user = next((row for row in users_db.values() if int(row["id"]) == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["role"] = str(payload.get("role", "user"))
    return {"user": user}


@router.get("/products")
async def admin_products():
    return {"items": list(products_db.values()), "total": len(products_db)}


@router.get("/orders")
async def admin_orders():
    return {"items": list(orders.values()), "total": len(orders)}


@router.get("/config")
async def configuration():
    return {"admin_email": ADMIN_EMAIL, "admin_password": ADMIN_PASSWORD, "database_url": DATABASE_URL, "jwt_secret": JWT_SECRET}


@router.get("/backup")
async def backup():
    return {"users": list(users_db.values()), "products": list(products_db.values()), "orders": list(orders.values())}
