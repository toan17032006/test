"""
Product Routes - Intentionally Vulnerable
Covers vulns: SQLi (#128), NoSQL Injection (#136), XSS (#171), IDOR (#97), Mass Assignment (#250)
"""
import re
import json
import csv
import io
from typing import Optional, List
from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter()

# In-memory product database (simulates DB)
products_db = {
    1: {
        "id": 1, "name": "iPhone 15 Pro Max", "description": "<b>Flagship iPhone</b>",
        "price": 29990000, "cost": 15000000,  # Internal cost exposed (vuln #651)
        "stock": 50, "category": "Electronics", "brand": "Apple",
        "sku": "IPHONE-15-PM", "weight": 0.221,
        "images": ["/uploads/iphone15.jpg"],
        "variants": [{"color": "Black Titanium", "storage": "256GB", "price": 29990000}],
        "is_active": True, "is_hidden": False,
        "admin_note": "Profit margin 40%",  # Sensitive business data (vuln #651)
        "supplier": "Apple Vietnam", "supplier_cost": 14000000,
    },
    2: {
        "id": 2, "name": "Samsung Galaxy S24 Ultra", "description": "Best Android flagship",
        "price": 27990000, "cost": 12000000,
        "stock": 30, "category": "Electronics", "brand": "Samsung",
        "sku": "SAMSUNG-S24U", "weight": 0.232,
        "images": ["/uploads/s24ultra.jpg"],
        "variants": [{"color": "Titanium Black", "storage": "256GB", "price": 27990000}],
        "is_active": True, "is_hidden": False,
        "admin_note": "High demand product",
        "supplier": "Samsung Vietnam", "supplier_cost": 11000000,
    },
    3: {
        "id": 3, "name": "MacBook Pro M3", "description": "Professional laptop",
        "price": 54990000, "cost": 30000000,
        "stock": 20, "category": "Laptops", "brand": "Apple",
        "sku": "MACBOOK-M3-PRO", "weight": 1.6,
        "images": ["/uploads/macbook.jpg"],
        "variants": [], "is_active": True, "is_hidden": False,
        "admin_note": "Best seller Q4",
        "supplier": "Apple Vietnam", "supplier_cost": 28000000,
    },
    4: {
        "id": 4, "name": "Áo Thun Nam Basic", "description": "Áo thun cotton 100%",
        "price": 199000, "cost": 80000,
        "stock": 200, "category": "Clothing", "brand": "VinFashion",
        "sku": "SHIRT-BASIC-001", "weight": 0.2,
        "images": ["/uploads/shirt.jpg"],
        "variants": [{"size": "M", "color": "Trắng"}, {"size": "L", "color": "Đen"}],
        "is_active": True, "is_hidden": False,
        "admin_note": "", "supplier": "Factory HN", "supplier_cost": 60000,
    },
    5: {
        "id": 5, "name": "Nike Air Force 1", "description": "Classic sneakers",
        "price": 2890000, "cost": 1200000,
        "stock": 100, "category": "Shoes", "brand": "Nike",
        "sku": "NIKE-AF1-WHT", "weight": 0.8,
        "images": ["/uploads/nike.jpg"],
        "variants": [{"size": "40"}, {"size": "41"}, {"size": "42"}],
        "is_active": True, "is_hidden": False,
        "admin_note": "High margin item",
        "supplier": "Nike SEA", "supplier_cost": 900000,
    },
}

reviews_db = {}  # product_id -> [reviews]
flash_sales_db = {
    1: {"product_id": 1, "original_price": 29990000, "sale_price": 24990000, "stock_limit": 10, "sold": 0}
}

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: str
    brand: str
    # Mass assignment fields - all accepted (vuln #250)
    cost: Optional[float] = None
    is_admin_product: Optional[bool] = False
    admin_note: Optional[str] = None
    supplier_cost: Optional[float] = None
    is_active: Optional[bool] = True
    hidden_discount: Optional[float] = 0  # Hidden discount

class ReviewCreate(BaseModel):
    content: str  # No XSS sanitization
    rating: int
    user_name: Optional[str] = "Anonymous"


@router.get("")
async def list_products(
    request: Request,
    search: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort: Optional[str] = "id",
    order: Optional[str] = "asc",
    limit: Optional[int] = None,  # No limit = unbounded (vuln #603)
    offset: Optional[int] = 0,
    page: Optional[int] = None,  # Unbounded pagination (vuln #603)
):
    """List products - SQL injection in search, unbounded pagination (vuln #128, #603)"""
    products = list(products_db.values())

    # SQL injection simulation in search (vuln #128)
    # In real: SELECT * FROM products WHERE name LIKE '%{search}%'
    if search:
        # ReDoS vulnerability (vuln #239, #587) - catastrophic backtracking
        try:
            # Vulnerable regex pattern
            pattern = re.compile(f".*{search}.*", re.IGNORECASE)  # ReDoS possible
            products = [p for p in products if pattern.search(p["name"])]
        except re.error:
            products = []

    if category:
        products = [p for p in products if p["category"].lower() == category.lower()]

    if min_price is not None:
        products = [p for p in products if p["price"] >= min_price]

    if max_price is not None:
        products = [p for p in products if p["price"] <= max_price]

    # SQL injection in sort parameter (vuln #128, #259)
    # ORDER BY {sort} {order} - injectable
    if sort not in ["id", "name", "price", "stock"]:
        # Injection reflected back (vuln #24)
        return {"error": f"Invalid sort field: {sort}", "hint": "Try: id, name, price, stock"}

    # Return ALL fields including sensitive ones (vuln #251)
    return {
        "products": products,  # Including cost, admin_note, supplier_cost (vuln #651)
        "total": len(products),
        "search_query": search,  # Reflected back (potential XSS context)
        "debug": {"sql": f"SELECT * FROM products WHERE name LIKE '%{search}%' ORDER BY {sort} {order}"},
    }


@router.get("/export")
async def export_products_csv(format: str = "csv"):
    """Export products - CSV injection (vuln #168)"""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Name", "Price", "Stock", "Cost", "Supplier Cost", "Admin Note"])

    for p in products_db.values():
        # CSV injection - name or admin_note can contain formulas (vuln #168)
        writer.writerow([
            p["id"],
            p["name"],  # Could be: =cmd|'/c calc'!A0
            p["price"],
            p["stock"],
            p["cost"],  # Sensitive data exposed
            p["supplier_cost"],  # Sensitive data exposed
            p["admin_note"],
        ])

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=products.csv"}
    )


@router.get("/flash-sale")
async def flash_sale():
    """Flash sale - race condition vulnerability (vuln #300, #305)"""
    return {"flash_sales": list(flash_sales_db.values()), "note": "Race condition possible - no locking"}


@router.get("/{product_id}")
async def get_product(product_id: int, request: Request):
    """Get product - IDOR, returns ALL fields including sensitive (vuln #97, #251)"""
    product = products_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

    # Return ALL fields including internal data (vuln #251, #651)
    return {
        "product": product,
        "internal_data": {
            "cost": product["cost"],
            "supplier_cost": product["supplier_cost"],
            "admin_note": product["admin_note"],
        }
    }


@router.post("")
async def create_product(data: ProductCreate, request: Request):
    """Create product - mass assignment, no auth check (vuln #250, #104)"""
    # No authentication check (vuln #104)
    # Mass assignment - all fields accepted including privileged ones (vuln #250)
    new_id = max(products_db.keys()) + 1 if products_db else 1
    product = {
        "id": new_id,
        "name": data.name,
        "description": data.description,  # XSS in description not sanitized (vuln #171)
        "price": data.price,
        "cost": data.cost,
        "stock": data.stock,
        "category": data.category,
        "brand": data.brand,
        "is_active": data.is_active,
        "is_admin_product": data.is_admin_product,  # Mass assignment
        "admin_note": data.admin_note,
        "supplier_cost": data.supplier_cost,
        "hidden_discount": data.hidden_discount,  # Mass assignment
        "images": [], "variants": [],
        "sku": f"SKU-{new_id}", "weight": 0,
    }
    products_db[new_id] = product
    return {"product": product, "message": "Product created"}


@router.put("/{product_id}")
async def update_product(product_id: int, data: dict, request: Request):
    """Update product - no ownership check, IDOR (vuln #97, #125)"""
    # No auth check
    # No ownership validation
    # HTTP method bypass - PUT works for anyone
    product = products_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Mass assignment - update any field (vuln #250)
    products_db[product_id].update(data)
    return {"product": products_db[product_id], "updated_fields": list(data.keys())}


@router.delete("/{product_id}")
async def delete_product(product_id: int, request: Request):
    """Delete product - no auth (vuln #104)"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    del products_db[product_id]
    return {"message": f"Product {product_id} deleted", "note": "No auth check performed"}


@router.get("/{product_id}/recommendations")
async def get_recommendations(product_id: int, url: Optional[str] = None):
    """Get recommendations - SSRF via external URL (vuln #198, #203)"""
    import httpx

    if url:
        # SSRF - fetch any URL including internal services (vuln #198)
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
                resp = await client.get(url)  # Fetch attacker-controlled URL
                return {"recommendations": resp.text[:1000], "url_fetched": url}
        except Exception as e:
            return {"error": str(e), "url_attempted": url}

    # Return based on category
    product = products_db.get(product_id, {})
    recs = [p for pid, p in products_db.items() if pid != product_id and p.get("category") == product.get("category")]
    return {"recommendations": recs[:4]}


@router.post("/{product_id}/review")
async def add_review(product_id: int, data: ReviewCreate, request: Request):
    """Add review - stored XSS (vuln #171, #177)"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")

    if product_id not in reviews_db:
        reviews_db[product_id] = []

    review = {
        "id": len(reviews_db[product_id]) + 1,
        "content": data.content,  # Stored without sanitization - XSS (vuln #171)
        "rating": data.rating,
        "user_name": data.user_name,  # Also unsanitized
        "created_at": "2024-01-01",
    }
    reviews_db[product_id].append(review)
    return {"review": review, "note": "Content stored without XSS sanitization"}


@router.get("/{product_id}/reviews")
async def get_reviews(product_id: int):
    """Get reviews - returns XSS payloads unsanitized (vuln #171)"""
    return {"reviews": reviews_db.get(product_id, []), "note": "Content rendered without escaping"}


@router.get("/{product_id}/qna")
async def get_qna(product_id: int, q: Optional[str] = None):
    """Q&A - reflected XSS in question (vuln #170)"""
    return {
        "product_id": product_id,
        "question": q,  # Reflected without sanitization (vuln #170)
        "answers": [],
        "xss_note": "Parameter q reflected without encoding",
    }
