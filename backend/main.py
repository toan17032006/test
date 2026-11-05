"""
VulnShop FastAPI Main Application
INTENTIONALLY VULNERABLE E-COMMERCE PLATFORM FOR PENTESTING
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
    description="VulnShop API - Intentionally Vulnerable E-Commerce for Pentesting",
    docs_url="/docs",        # Swagger UI - no auth (vuln #19)
    redoc_url="/redoc",      # ReDoc - no auth
    openapi_url="/openapi.json",
)

# ─── CORS Middleware (intentionally misconfigured - vuln #187) ───────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # vuln #187 - CORS Origin Reflection
    allow_credentials=True,         # vuln #189 - with credentials=True + *origins = dangerous
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
app.include_router(auth_router, prefix="/api/v2/auth", tags=["Authentication v2"])  # API versioning bypass (vuln #253)
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
    """WebSocket - no auth check (vuln #271, #272)"""
    await ws.accept()
    active_connections.append(ws)
    # No authentication or authorization
    try:
        while True:
            data = await ws.receive_text()
            # Reflect data back (potential XSS via WebSocket)
            await ws.send_text(json.dumps({"type": "echo", "data": data}))
            # Broadcast to ALL connected clients (no isolation - vuln #272)
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
    """Admin WebSocket - no auth check (vuln #271)"""
    await ws.accept()
    # Send all admin data to anyone who connects
    await ws.send_text(json.dumps({
        "type": "admin_data",
        "users_count": 1500,
        "revenue": 5000000,
        "db_url": DATABASE_URL,  # Intentional exposure
        "admin_password": ADMIN_PASSWORD,
    }))

# ─── Information Disclosure Endpoints ────────────────────────────────────────

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - technology stack disclosure (vuln #8)"""
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
    """Health check - internal IP disclosure (vuln #26)"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "hostname": socket.gethostname(),
        "internal_ip": socket.gethostbyname(socket.gethostname()),
        "pid": os.getpid(),
        "platform": platform.platform(),
        "python_version": sys.version,
        "database_url": DATABASE_URL,  # Credential exposure
        "redis_url": REDIS_URL,
        "environment": ENVIRONMENT,
    }

@app.get("/debug", tags=["Debug"])
async def debug_info():
    """Debug endpoint - full system info disclosure (vuln #10, #26)"""
    import subprocess
    env_vars = dict(os.environ)
    return {
        "debug": DEBUG,
        "environment_variables": env_vars,  # All env vars exposed
        "python_path": sys.path,
        "platform": {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "aws_key": AWS_ACCESS_KEY_ID,  # Cloud credential exposure (vuln #435)
        "aws_secret": AWS_SECRET_ACCESS_KEY,
        "jwt_secret": JWT_SECRET,
        "stripe_key": STRIPE_SECRET_KEY,
        "db_url": DATABASE_URL,
        "admin_password": ADMIN_PASSWORD,
    }

@app.get("/metrics", tags=["Metrics"])
async def metrics():
    """Prometheus-style metrics - no auth (vuln #570)"""
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
        "secret_key": SECRET_KEY,  # Intentional exposure
    }

@app.get("/phpinfo.php", tags=["Info"])
async def phpinfo():
    """Fake phpinfo for fingerprinting (vuln #9)"""
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
    """Exposed .env file (vuln #17)"""
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
    """Database backup exposure (vuln #15, #410)"""
    return {"message": "DB backup available", "url": "/uploads/backup_2024.sql", "note": "Contains full database dump"}

@app.get("/api/internal/db-query", tags=["Internal"])
async def internal_db_query(q: str = "SELECT * FROM users"):
    """Internal DB query endpoint - no auth (vuln #401, #406)"""
    # This would actually execute queries in real implementation
    return {"query": q, "note": "Direct DB query endpoint exposed", "warning": "SQL Injection possible here"}

@app.get("/swagger.json", tags=["Docs"])
async def swagger_json():
    """Swagger exposure (vuln #19)"""
    return app.openapi()

@app.get("/graphql", tags=["GraphQL"])
async def graphql_info():
    """GraphQL introspection info (vuln #20)"""
    return {
        "graphql_url": "http://localhost:4000/graphql",
        "introspection": True,
        "subscriptions": True,
    }

# ─── Error Handlers (stack trace disclosure - vuln #25) ─────────────────────

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Return full stack trace (vuln #25)"""
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "type": type(exc).__name__,
            "traceback": traceback.format_exc(),  # Full stack trace exposed
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
            # Server version disclosure in error (vuln #7)
            "server": f"VulnShop/{APP_VERSION} FastAPI/{FRAMEWORK_VERSION}",
        },
        headers={
            "X-Powered-By": f"FastAPI/{FRAMEWORK_VERSION}",  # vuln #7
            "Server": f"uvicorn/0.24.0",
            "X-Debug": str(DEBUG),
        }
    )

# ─── Request Logging Middleware (logs passwords - vuln #558) ─────────────────

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests including sensitive data (vuln #558, #559, #560)"""
    body = b""
    try:
        body = await request.body()
    except:
        pass

    # Log everything including passwords and tokens
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),  # Auth headers logged
        "body": body.decode("utf-8", errors="ignore"),  # Passwords logged
        "client_ip": request.client.host if request.client else "unknown",
    }

    # CRLF injection in logs (vuln #562)
    user_agent = request.headers.get("User-Agent", "")
    print(f"[ACCESS] {datetime.utcnow()} - {request.method} {request.url} - UA: {user_agent}")
    print(f"[BODY] {log_entry['body'][:500]}")  # Passwords appear here

    # Add security-disclosing headers to response
    response = await call_next(request)
    response.headers["X-Powered-By"] = f"FastAPI/{FRAMEWORK_VERSION}"
    response.headers["Server"] = "vulnshop/1.0"
    response.headers["X-Debug-Mode"] = str(DEBUG)
    # No security headers added (vuln #227)
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
