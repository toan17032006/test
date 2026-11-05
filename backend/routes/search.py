"""Product search endpoints over the local sample catalog."""

from fastapi import APIRouter, Query

from routes.products import products_db

router = APIRouter()


@router.get("")
async def search(q: str = "", category: str | None = None, limit: int = Query(20, ge=1, le=100)):
    query = q.casefold()
    rows = [row for row in products_db.values() if query in row["name"].casefold() or query in row.get("description", "").casefold()]
    if category:
        rows = [row for row in rows if row["category"].casefold() == category.casefold()]
    return {"items": rows[:limit], "total": len(rows), "query": q}


@router.get("/suggest")
async def suggestions(q: str = ""):
    rows = [row["name"] for row in products_db.values() if q.casefold() in row["name"].casefold()]
    return {"suggestions": rows[:8]}
