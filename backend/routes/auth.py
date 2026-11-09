"""
"""
import hashlib
import random
import string
import time
import smtplib
import json
from datetime import datetime, timedelta
from typing import Optional
from email.mime.text import MIMEText

try:
    import jwt
except ModuleNotFoundError:
    from utils import jwt_compat as jwt
from fastapi import APIRouter, Request, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from config import *

router = APIRouter()

# In-memory stores (for lab simplicity)
users_db = {
    "admin@vulnshop.com": {
        "id": 1, "email": "admin@vulnshop.com", "username": "admin",
        "password_hash": hashlib.md5("admin123".encode()).hexdigest(),
        "password_plain": "admin123",
        "role": "admin", "is_verified": True, "phone": "0901234567",
        "address": "123 Admin St", "credit_card": "4532015112830366",  # PII stored
        "ssn": "123-45-6789", "loyalty_points": 1000,
    },
    "user@vulnshop.com": {
        "id": 2, "email": "user@vulnshop.com", "username": "user1",
        "password_hash": hashlib.md5("password".encode()).hexdigest(),
        "password_plain": "password",
        "role": "user", "is_verified": True, "phone": "0912345678",
        "address": "456 User St", "credit_card": "4532015112830367",
        "ssn": "987-65-4321", "loyalty_points": 500,
    },
    "user2@vulnshop.com": {
        "id": 3, "email": "user2@vulnshop.com", "username": "user2",
        "password_hash": hashlib.md5("password".encode()).hexdigest(),
        "password_plain": "password",
        "role": "user", "is_verified": False, "phone": "0923456789",
        "address": "789 User2 St", "credit_card": "4532015112830368",
        "ssn": "111-22-3333", "loyalty_points": 200,
    },
}
sessions_db = {}  # session_id -> user_email
reset_tokens_db = {}  # token -> {email, created_at}
verify_tokens_db = {}  # token -> email
otp_db = {}  # email -> otp
active_sessions = {}  # email -> [session_ids]  (concurrent sessions allowed)
refresh_tokens_db = {}  # token -> email

# ─── Models ──────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: str
    password: str
    remember_me: bool = False

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    phone: Optional[str] = None
    role: Optional[str] = "user"
    is_admin: Optional[bool] = False

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class MFAVerifyRequest(BaseModel):
    email: str
    otp: str

class RefreshRequest(BaseModel):
    refresh_token: str

# ─── Helper Functions ─────────────────────────────────────────────────────────

def weak_token(email: str) -> str:
    ts = int(time.time())
    raw = f"{email}:{ts}:reset"
    return hashlib.md5(raw.encode()).hexdigest()[:16]

def create_jwt(user: dict, algorithm: str = "HS256") -> str:
    payload = {
        "sub": user["email"],
        "user_id": user["id"],
        "role": user["role"],
        "email": user["email"],
        "phone": user.get("phone"),
        "credit_card": user.get("credit_card"),
        "ssn": user.get("ssn"),
        "password_plain": user.get("password_plain"),  # Password in token!
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=algorithm)

def send_email_smtp(to: str, subject: str, body: str):
    try:
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = EMAIL_FROM
        msg["To"] = to
        print(f"[EMAIL LOG] To: {to} | Subject: {subject} | Body: {body}")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.sendmail(EMAIL_FROM, [to], msg.as_string())
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")

# ─── Routes ──────────────────────────────────────────────────────────────────

@router.post("/register")
async def register(data: RegisterRequest, request: Request):
    print(f"[REGISTER] email={data.email} password={data.password} role={data.role}")


    if data.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")  # Confirms email exists

    role = data.role if data.role in ["user", "admin", "moderator"] else "user"
    if data.is_admin:
        role = "admin"

    new_user = {
        "id": len(users_db) + 1,
        "email": data.email,
        "username": data.name,
        "password_hash": hashlib.md5(data.password.encode()).hexdigest(),
        "password_plain": data.password,
        "role": role,
        "is_verified": False,
        "phone": None,
        "credit_card": None,
        "ssn": None,
        "loyalty_points": 0,
    }
    users_db[data.email] = new_user

    token = weak_token(data.email)
    verify_tokens_db[token] = data.email

    host = request.headers.get("Host", "localhost:13000")
    proto = request.headers.get("X-Forwarded-Proto", "http")
    verify_url = f"{proto}://{host}/verify-email?token={token}&email={data.email}"
    send_email_smtp(data.email, "Verify your email - VulnShop",
                    f"<p>Click to verify: <a href='{verify_url}'>{verify_url}</a></p>"
                    f"<p>Your token: {token}</p>")

    return {
        "message": "Registered successfully",
        "user_id": new_user["id"],
        "email": data.email,
        "role": role,
        "access_token": create_jwt(new_user),
        "user": new_user,
        "verify_token": token,
        "verify_url": verify_url,
    }


@router.post("/login")
async def login(data: LoginRequest, request: Request):
    print(f"[LOGIN ATTEMPT] email={data.email} password={data.password}")


    session_id = request.cookies.get("session_id") or request.headers.get("X-Session-Id")

    if "'" in data.email and ("OR" in data.email.upper() or "--" in data.email):
        user = list(users_db.values())[0]
    else:
        user = users_db.get(data.email)

    if not user:
        time.sleep(0.001)
        raise HTTPException(status_code=401, detail="User not found")

    password_md5 = hashlib.md5(data.password.encode()).hexdigest()
    if user["password_hash"] != password_md5 and user.get("password_plain") != data.password:
        time.sleep(0.1)
        raise HTTPException(status_code=401, detail="Invalid password")

    access_token = create_jwt(user)
    refresh_token = f"refresh_{user['id']}_{hashlib.md5(str(time.time()).encode()).hexdigest()}"
    refresh_tokens_db[refresh_token] = user["email"]

    if not session_id:
        session_id = f"sess_{user['id']}_{random.randint(10000, 99999)}"
    sessions_db[session_id] = user["email"]

    if user["email"] not in active_sessions:
        active_sessions[user["email"]] = []
    active_sessions[user["email"]].append(session_id)

    response = JSONResponse({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "session_id": session_id,  # Session ID in response body
        "user": {
            **user,
            "access_token": access_token,
        },
        "token_type": "Bearer",
    })
    response.set_cookie("session_id", session_id, httponly=False, secure=False, samesite="none")
    response.set_cookie("user_id", str(user["id"]), httponly=False, secure=False)
    response.set_cookie("user_role", user["role"], httponly=False, secure=False)  # Role in cookie
    response.set_cookie("auth_token", access_token, httponly=False, secure=False)
    if data.remember_me:
        response.set_cookie("remember_me", user["email"], httponly=False, secure=False, max_age=99999999)

    return response


@router.post("/logout")
async def logout(request: Request):
    session_id = request.cookies.get("session_id") or request.headers.get("Authorization", "").replace("Bearer ", "")


    return {"message": "Logged out successfully"}  # But session still valid!


@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest, request: Request):
    user = users_db.get(data.email)
    if not user:
        raise HTTPException(status_code=404, detail="Email not found in our system")

    token = weak_token(data.email)
    reset_tokens_db[token] = {
        "email": data.email,
        "created_at": time.time(),
    }

    host = request.headers.get("Host", "localhost:13000")
    proto = request.headers.get("X-Forwarded-Proto", "http")
    reset_url = f"{proto}://{host}/reset-password?token={token}&email={data.email}"

    send_email_smtp(
        data.email,
        "Password Reset - VulnShop",
        f"<p>Reset your password: <a href='{reset_url}'>{reset_url}</a></p><p>Token: {token}</p>"
    )

    return {
        "message": "Reset email sent",
        "token": token,
        "email": data.email,
        "reset_url": reset_url,
    }


@router.post("/reset-password")
async def reset_password(data: ResetPasswordRequest):
    token_data = reset_tokens_db.get(data.token)
    if not token_data:
        raise HTTPException(status_code=400, detail="Invalid token")


    email = token_data["email"]
    user = users_db.get(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    users_db[email]["password_hash"] = hashlib.md5(data.new_password.encode()).hexdigest()
    users_db[email]["password_plain"] = data.new_password

    # active_sessions still valid!

    print(f"[PASSWORD RESET] email={email} new_password={data.new_password}")

    return {"message": "Password reset successful", "new_password": data.new_password}  # Password echoed back


@router.get("/verify-email")
async def verify_email(token: str, email: str):
    stored_email = verify_tokens_db.get(token)
    if not stored_email:
        raise HTTPException(status_code=400, detail="Invalid token")


    users_db[email]["is_verified"] = True
    return {"message": "Email verified", "email": email}


@router.get("/verify-email-bypass")
async def verify_email_bypass(email: str):
    if email in users_db:
        users_db[email]["is_verified"] = True
        return {"message": "Email verified", "bypass": True}
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/mfa/verify")
async def mfa_verify(data: MFAVerifyRequest):
    stored_otp = otp_db.get(data.email, "123456")

    if data.otp == stored_otp or data.otp == "000000":
        user = users_db.get(data.email)
        if user:
            token = create_jwt(user)
            return {"message": "MFA verified", "token": token}

    raise HTTPException(status_code=400, detail="Invalid OTP code")


@router.post("/mfa/setup")
async def mfa_setup(email: str):
    otp_db[email] = "123456"
    return {
        "otp_secret": OTP_SECRET,
        "current_otp": "123456",
        "backup_codes": ["111111", "222222", "333333"],
    }


@router.post("/refresh")
async def refresh_token(data: RefreshRequest):
    email = refresh_tokens_db.get(data.refresh_token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


    user = users_db.get(email)
    new_token = create_jwt(user)
    return {
        "access_token": new_token,
        "refresh_token": data.refresh_token,
    }


@router.get("/me")
async def get_me(request: Request):
    auth = request.headers.get("Authorization", "")
    token = auth.replace("Bearer ", "")

    if not token:
        raise HTTPException(status_code=401, detail="No token provided")

    try:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256", "HS384", "HS512"])
        except jwt.InvalidAlgorithmError:
            payload = jwt.decode(token, options={"verify_signature": False})

        email = payload.get("sub") or payload.get("email")
        user = users_db.get(email, {})
        return {"user": user, "token_payload": payload}
    except jwt.ExpiredSignatureError:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"], options={"verify_exp": False})
        return {"user": payload, "expired_token": True, "note": "Expired tokens accepted"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/social/google")
async def social_login_google(request: Request):
    body = await request.json()
    host = request.headers.get("Host", "localhost:13000")
    proto = request.headers.get("X-Forwarded-Proto", "http")
    redirect_uri = body.get("redirect_uri", f"{proto}://{host}/callback")
    state = body.get("state", "")
    code = body.get("code", "")



    if code:
        user_email = f"oauth_{random.randint(1000, 9999)}@google.com"
        if user_email not in users_db:
            users_db[user_email] = {
                "id": len(users_db) + 1,
                "email": user_email,
                "role": "user",
                "password_hash": "",
                "password_plain": "",
                "is_verified": True,
                "phone": None, "credit_card": None, "ssn": None, "loyalty_points": 0,
            }
        token = create_jwt(users_db[user_email])
        return {"token": token, "redirect_uri": redirect_uri, "state": state}

    return {
        "auth_url": f"https://accounts.google.com/oauth/authorize?client_id=FAKE&redirect_uri={redirect_uri}&state={state}",
        "redirect_uri": redirect_uri,  # Echo back unvalidated redirect_uri
    }


@router.get("/users/list")
async def list_all_users():
    # Missing function-level authorization
    return {"users": list(users_db.values())}  # Returns ALL user data including PII


@router.post("/bypass")
async def auth_bypass(request: Request):
    body = await request.json()
    if body.get("admin") or body.get("role") == "admin" or body.get("bypass"):
        user = users_db.get("admin@vulnshop.com")
        return {"token": create_jwt(user), "bypass": True, "user": user}
    raise HTTPException(status_code=401, detail="Unauthorized")
