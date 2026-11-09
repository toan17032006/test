"""
"""
import os
import sys
import json
import traceback
import platform
import socket
from datetime import datetime
from typing import Any

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from config import *

# ─── App Init ───────────────────────────────────────────────────────────────
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="VulnShop API - E-Commerce Platform",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# ─── Static Files ────────────────────────────────────────────────────────────
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# ─── Import Routers ──────────────────────────────────────────────────────────
from routes.auth import router as auth_router
from routes.products import router as products_router
from routes.cart import router as cart_router
from routes.orders import router as orders_router
from routes.payment import router as payment_router
from routes.users import router as users_router
from routes.admin import router as admin_router
from routes.files import router as files_router
from routes.webhooks import router as webhooks_router
from routes.search import router as search_router
from routes.coupons import router as coupons_router
from routes.notifications import router as notifications_router

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(auth_router, prefix="/api/v2/auth", tags=["Authentication v2"])
app.include_router(products_router, prefix="/api/v1/products", tags=["Products"])
app.include_router(cart_router, prefix="/api/v1/cart", tags=["Cart"])
app.include_router(orders_router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(payment_router, prefix="/api/v1/payment", tags=["Payment"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(files_router, prefix="/api/v1/files", tags=["Files"])
app.include_router(webhooks_router, prefix="/api/v1/webhooks", tags=["Webhooks"])
app.include_router(search_router, prefix="/api/v1/search", tags=["Search"])
app.include_router(coupons_router, prefix="/api/v1/coupons", tags=["Coupons"])
app.include_router(notifications_router, prefix="/api/v1/notify", tags=["Notifications"])

# ─── WebSocket Manager ───────────────────────────────────────────────────────
active_connections: list[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    active_connections.append(ws)
    try:
        while True:
            data = await ws.receive_text()
            await ws.send_text(json.dumps({"type": "echo", "data": data}))
            for conn in active_connections:
                if conn != ws:
                    try:
                        await conn.send_text(json.dumps({"type": "broadcast", "data": data}))
                    except:
                        pass
    except WebSocketDisconnect:
        active_connections.remove(ws)

@app.websocket("/ws/admin")
async def admin_ws(ws: WebSocket):
    await ws.accept()
    await ws.send_text(json.dumps({
        "type": "admin_data",
        "users_count": 1500,
        "revenue": 5000000,
        "db_url": DATABASE_URL,
        "admin_password": ADMIN_PASSWORD,
    }))

# ─── Information Disclosure Endpoints ────────────────────────────────────────

@app.get("/", tags=["Root"])
async def root():
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "framework": FRAMEWORK_VERSION,
        "python": PYTHON_VERSION,
        "database": DB_VERSION,
        "environment": ENVIRONMENT,
        "debug": DEBUG,
        "docs": "/docs",
        "admin": "/api/v1/admin",
        "graphql": "http://graphql:4000/graphql",
    }

@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "hostname": socket.gethostname(),
        "internal_ip": socket.gethostbyname(socket.gethostname()),
        "pid": os.getpid(),
        "platform": platform.platform(),
        "python_version": sys.version,
        "database_url": DATABASE_URL,
        "redis_url": REDIS_URL,
        "environment": ENVIRONMENT,
    }

@app.get("/debug", tags=["Debug"])
async def debug_info():
    import subprocess
    env_vars = dict(os.environ)
    return {
        "debug": DEBUG,
        "environment_variables": env_vars,
        "python_path": sys.path,
        "platform": {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "aws_key": AWS_ACCESS_KEY_ID,
        "aws_secret": AWS_SECRET_ACCESS_KEY,
        "jwt_secret": JWT_SECRET,
        "stripe_key": STRIPE_SECRET_KEY,
        "db_url": DATABASE_URL,
        "admin_password": ADMIN_PASSWORD,
    }

@app.get("/metrics", tags=["Metrics"])
async def metrics():
    return {
        "vulnshop_requests_total": 15420,
        "vulnshop_active_users": 234,
        "vulnshop_revenue_total": 50000000,
        "vulnshop_orders_pending": 45,
        "db_connections_active": 12,
        "redis_memory_used": "256MB",
        "internal_endpoints": [
            "/api/v1/admin/users",
            "/api/v1/admin/config",
            "/api/v1/admin/backup",
            "/api/internal/db-query",
        ],
        "secret_key": SECRET_KEY,
    }

@app.get("/phpinfo.php", tags=["Info"])
async def phpinfo():
    return HTMLResponse("""
    <html><body>
    <h1>PHP Version 8.2.0</h1>
    <table>
    <tr><td>Server API</td><td>Apache 2.4.54</td></tr>
    <tr><td>Server Software</td><td>Apache/2.4.54 (Ubuntu)</td></tr>
    <tr><td>DB_PASSWORD</td><td>postgres123</td></tr>
    <tr><td>SECRET_KEY</td><td>super-secret-key-12345</td></tr>
    </table>
    </body></html>
    """)

@app.get("/.env", tags=["Info"])
async def env_file():
    return HTMLResponse(f"""SECRET_KEY={SECRET_KEY}
JWT_SECRET={JWT_SECRET}
DATABASE_URL={DATABASE_URL}
AWS_ACCESS_KEY_ID={AWS_ACCESS_KEY_ID}
AWS_SECRET_ACCESS_KEY={AWS_SECRET_ACCESS_KEY}
STRIPE_SECRET_KEY={STRIPE_SECRET_KEY}
ADMIN_PASSWORD={ADMIN_PASSWORD}
SMTP_PASS={SMTP_PASS}
""", media_type="text/plain")

@app.get("/backup/db.sql", tags=["Backup"])
async def db_backup():
    return {"message": "DB backup available", "url": "/uploads/backup_2024.sql", "note": "Contains full database dump"}

@app.get("/api/internal/db-query", tags=["Internal"])
async def internal_db_query(q: str = "SELECT * FROM users"):
    return {"query": q, "result": []}

@app.get("/swagger.json", tags=["Docs"])
async def swagger_json():
    return app.openapi()

@app.get("/graphql", tags=["GraphQL"])
async def graphql_info():
    return {
        "graphql_url": "http://localhost:4000/graphql",
        "introspection": True,
        "subscriptions": True,
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "type": type(exc).__name__,
            "traceback": traceback.format_exc(),
            "request_path": str(request.url),
            "method": request.method,
            "headers": dict(request.headers),
            "server": {
                "db_url": DATABASE_URL,
                "secret": SECRET_KEY,
            }
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url),
            "server": f"VulnShop/{APP_VERSION} FastAPI/{FRAMEWORK_VERSION}",
        },
        headers={
            "X-Powered-By": f"FastAPI/{FRAMEWORK_VERSION}",
            "Server": f"uvicorn/0.24.0",
            "X-Debug": str(DEBUG),
        }
    )


@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = b""
    try:
        body = await request.body()
    except:
        pass

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),  # Auth headers logged
        "body": body.decode("utf-8", errors="ignore"),  # Passwords logged
        "client_ip": request.client.host if request.client else "unknown",
    }

    user_agent = request.headers.get("User-Agent", "")
    print(f"[ACCESS] {datetime.utcnow()} - {request.method} {request.url} - UA: {user_agent}")
    print(f"[BODY] {log_entry['body'][:500]}")  # Passwords appear here

    # Add security-disclosing headers to response
    response = await call_next(request)
    response.headers["X-Powered-By"] = f"FastAPI/{FRAMEWORK_VERSION}"
    response.headers["Server"] = "vulnshop/1.0"
    response.headers["X-Debug-Mode"] = str(DEBUG)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug",
    )
