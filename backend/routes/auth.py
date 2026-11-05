"""
Authentication Routes - Intentionally Vulnerable
Covers vulns: #31-95 (Authentication Vulnerabilities)
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
        "password_hash": hashlib.md5("admin123".encode()).hexdigest(),  # vuln #372 MD5
        "password_plain": "admin123",  # Plaintext stored! vuln #372
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
    role: Optional[str] = "user"  # Mass assignment - anyone can set role (vuln #103)
    is_admin: Optional[bool] = False  # Mass assignment vuln

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
    """Predictable token generation (vuln #52, #378)"""
    # Token based on email + timestamp truncated to seconds = predictable
    ts = int(time.time())
    raw = f"{email}:{ts}:reset"
    return hashlib.md5(raw.encode()).hexdigest()[:16]  # Short MD5 = predictable

def create_jwt(user: dict, algorithm: str = "HS256") -> str:
    """Create JWT - stores sensitive data in payload (vuln #81)"""
    payload = {
        "sub": user["email"],
        "user_id": user["id"],
        "role": user["role"],
        "email": user["email"],
        "phone": user.get("phone"),          # PII in token (vuln #81)
        "credit_card": user.get("credit_card"),  # PII in token (vuln #81)
        "ssn": user.get("ssn"),              # PII in token (vuln #81)
        "password_plain": user.get("password_plain"),  # Password in token!
        "iat": datetime.utcnow(),
        # No exp = never expires (vuln #77)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=algorithm)

def send_email_smtp(to: str, subject: str, body: str):
    """Send email via MailHog - SMTP injection possible (vuln #161)"""
    try:
        msg = MIMEText(body, "html")
        # SMTP injection via subject (vuln #161)
        msg["Subject"] = subject  # Not sanitized
        msg["From"] = EMAIL_FROM
        msg["To"] = to  # Not sanitized - SMTP injection
        # Log email including content (vuln #559)
        print(f"[EMAIL LOG] To: {to} | Subject: {subject} | Body: {body}")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.sendmail(EMAIL_FROM, [to], msg.as_string())
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")

# ─── Routes ──────────────────────────────────────────────────────────────────

@router.post("/register")
async def register(data: RegisterRequest, request: Request):
    """Register - weak password policy, email enumeration (vuln #31, #34, #35)"""
    # Log registration data including password (vuln #558)
    print(f"[REGISTER] email={data.email} password={data.password} role={data.role}")

    # Weak password policy - no length/complexity check (vuln #31)
    # Password "1" is accepted

    # Email enumeration - different error messages (vuln #35)
    if data.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")  # Confirms email exists

    # Mass assignment - role can be set by user (vuln #103)
    role = data.role if data.role in ["user", "admin", "moderator"] else "user"
    if data.is_admin:
        role = "admin"  # Privilege escalation via mass assignment

    new_user = {
        "id": len(users_db) + 1,
        "email": data.email,
        "username": data.name,
        "password_hash": hashlib.md5(data.password.encode()).hexdigest(),  # MD5! vuln #372
        "password_plain": data.password,  # Store plaintext vuln #372
        "role": role,
        "is_verified": False,
        "phone": None,
        "credit_card": None,
        "ssn": None,
        "loyalty_points": 0,
    }
    users_db[data.email] = new_user

    # Generate predictable token (vuln #52)
    token = weak_token(data.email)
    verify_tokens_db[token] = data.email

    # Token in email URL (sensitive data in URL - vuln #393)
    verify_url = f"http://localhost:3000/verify-email?token={token}&email={data.email}"
    send_email_smtp(data.email, "Verify your email - VulnShop",
                    f"<p>Click to verify: <a href='{verify_url}'>{verify_url}</a></p>"
                    f"<p>Your token: {token}</p>")

    return {
        "message": "Registered successfully",
        "user_id": new_user["id"],
        "email": data.email,
        "role": role,  # Role disclosed
        "verify_token": token,  # Token in response (vuln #51)
        "verify_url": verify_url,
    }


@router.post("/login")
async def login(data: LoginRequest, request: Request):
    """Login - SQL injection sim, timing attack, brute force possible (vuln #38, #64, #65, #66)"""
    # Log credentials (vuln #558)
    print(f"[LOGIN ATTEMPT] email={data.email} password={data.password}")

    # No rate limiting (vuln #38, #41)
    # No CAPTCHA (vuln #43)

    # Session fixation - use existing session ID if provided (vuln #65)
    session_id = request.cookies.get("session_id") or request.headers.get("X-Session-Id")

    # SQL injection simulation in login (vuln #128)
    # In real DB: SELECT * FROM users WHERE email='{email}' AND password='{password}'
    # With: email = "admin@vulnshop.com' OR '1'='1'--" → bypasses auth
    if "'" in data.email and ("OR" in data.email.upper() or "--" in data.email):
        # Simulate SQLi bypass
        user = list(users_db.values())[0]  # Return first user (admin)
        print(f"[SQL INJECTION DETECTED - ALLOWING] {data.email}")
        # vuln: should block but doesn't
    else:
        user = users_db.get(data.email)

    # Username enumeration via timing (vuln #34)
    if not user:
        # Different response time for non-existent vs wrong password
        time.sleep(0.001)  # Faster for non-existent (timing attack)
        raise HTTPException(status_code=401, detail="User not found")  # Confirms non-existence

    # Password check using MD5 (vuln #372)
    password_md5 = hashlib.md5(data.password.encode()).hexdigest()
    if user["password_hash"] != password_md5 and user.get("password_plain") != data.password:
        time.sleep(0.1)
        raise HTTPException(status_code=401, detail="Invalid password")  # Different msg = enumeration

    # Create JWT with sensitive data (vuln #81)
    access_token = create_jwt(user)
    # Refresh token - never expires, can be reused (vuln #82)
    refresh_token = f"refresh_{user['id']}_{hashlib.md5(str(time.time()).encode()).hexdigest()}"
    refresh_tokens_db[refresh_token] = user["email"]

    # Session management - session NOT invalidated if exists (vuln #68, #70)
    if not session_id:
        session_id = f"sess_{user['id']}_{random.randint(10000, 99999)}"
    sessions_db[session_id] = user["email"]

    # Concurrent sessions allowed (vuln #70)
    if user["email"] not in active_sessions:
        active_sessions[user["email"]] = []
    active_sessions[user["email"]].append(session_id)

    # Remember me - insecure persistent cookie (vuln #62)
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
    # Insecure cookie (vuln #71) - no Secure, no HttpOnly, SameSite=None
    response.set_cookie("session_id", session_id, httponly=False, secure=False, samesite="none")
    response.set_cookie("user_id", str(user["id"]), httponly=False, secure=False)
    response.set_cookie("user_role", user["role"], httponly=False, secure=False)  # Role in cookie
    response.set_cookie("auth_token", access_token, httponly=False, secure=False)
    if data.remember_me:
        # Insecure remember me (vuln #62)
        response.set_cookie("remember_me", user["email"], httponly=False, secure=False, max_age=99999999)

    return response


@router.post("/logout")
async def logout(request: Request):
    """Logout - session NOT invalidated (vuln #68)"""
    session_id = request.cookies.get("session_id") or request.headers.get("Authorization", "").replace("Bearer ", "")

    # Session NOT removed from server (vuln #68)
    # sessions_db.pop(session_id, None)  <-- intentionally commented out

    return {"message": "Logged out successfully"}  # But session still valid!


@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest, request: Request):
    """Forgot password - host header injection (vuln #56), token exposure (vuln #51)"""
    # Email enumeration - confirm if email exists (vuln #35)
    user = users_db.get(data.email)
    if not user:
        raise HTTPException(status_code=404, detail="Email not found in our system")  # Enumeration

    # Predictable token (vuln #52)
    token = weak_token(data.email)
    reset_tokens_db[token] = {
        "email": data.email,
        "created_at": time.time(),
        # No expiry set (vuln #54)
    }

    # Host Header Injection (vuln #56) - use Host header for reset URL
    host = request.headers.get("Host", "localhost:3000")  # Attacker controls this
    proto = request.headers.get("X-Forwarded-Proto", "http")
    reset_url = f"{proto}://{host}/reset-password?token={token}&email={data.email}"

    # Token leaked in response (vuln #51)
    send_email_smtp(
        data.email,
        "Password Reset - VulnShop",
        f"<p>Reset your password: <a href='{reset_url}'>{reset_url}</a></p><p>Token: {token}</p>"
    )

    return {
        "message": "Reset email sent",
        "token": token,          # Token in response body (vuln #51)
        "email": data.email,
        "reset_url": reset_url,  # URL exposed in response
    }


@router.post("/reset-password")
async def reset_password(data: ResetPasswordRequest):
    """Reset password - token reuse, never expires (vuln #53, #54)"""
    token_data = reset_tokens_db.get(data.token)
    if not token_data:
        raise HTTPException(status_code=400, detail="Invalid token")

    # No expiry check (vuln #54) - tokens never expire
    # Token NOT deleted after use (vuln #53) - can be reused

    email = token_data["email"]
    user = users_db.get(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Weak new password accepted (vuln #31)
    users_db[email]["password_hash"] = hashlib.md5(data.new_password.encode()).hexdigest()
    users_db[email]["password_plain"] = data.new_password

    # Sessions NOT invalidated after password change (vuln #69)
    # active_sessions still valid!

    # Log password change (vuln #558)
    print(f"[PASSWORD RESET] email={email} new_password={data.new_password}")

    return {"message": "Password reset successful", "new_password": data.new_password}  # Password echoed back


@router.get("/verify-email")
async def verify_email(token: str, email: str):
    """Email verification - token reuse (vuln #57, #58)"""
    stored_email = verify_tokens_db.get(token)
    if not stored_email:
        raise HTTPException(status_code=400, detail="Invalid token")

    # Token NOT deleted = can be reused (vuln #58)
    # verify_tokens_db.pop(token)  <-- commented out

    users_db[email]["is_verified"] = True
    return {"message": "Email verified", "email": email}


@router.get("/verify-email-bypass")
async def verify_email_bypass(email: str):
    """Email verification bypass (vuln #59) - no token needed"""
    if email in users_db:
        users_db[email]["is_verified"] = True
        return {"message": "Email verified", "bypass": True}
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/mfa/verify")
async def mfa_verify(data: MFAVerifyRequest):
    """MFA verify - OTP brute force, replay (vuln #44, #46, #47, #48)"""
    # No rate limiting on OTP (vuln #46)
    # Predictable OTP (vuln #48)
    stored_otp = otp_db.get(data.email, "123456")  # Default OTP = "123456" (predictable)

    # OTP not deleted after use (vuln #47 - replay)
    if data.otp == stored_otp or data.otp == "000000":  # Backdoor OTP (vuln #44)
        user = users_db.get(data.email)
        if user:
            token = create_jwt(user)
            return {"message": "MFA verified", "token": token}

    # Different error for wrong OTP vs expired (enumeration)
    raise HTTPException(status_code=400, detail="Invalid OTP code")


@router.post("/mfa/setup")
async def mfa_setup(email: str):
    """MFA setup - hardcoded secret (vuln #376)"""
    otp_db[email] = "123456"  # Predictable OTP (vuln #48)
    return {
        "otp_secret": OTP_SECRET,  # Hardcoded secret exposed
        "current_otp": "123456",
        "backup_codes": ["111111", "222222", "333333"],  # Weak backup codes
    }


@router.post("/refresh")
async def refresh_token(data: RefreshRequest):
    """Refresh token - reuse allowed, rotation failure (vuln #82, #83)"""
    email = refresh_tokens_db.get(data.refresh_token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Token NOT rotated (vuln #83) - same token works forever
    # refresh_tokens_db.pop(data.refresh_token)  <-- commented out

    user = users_db.get(email)
    new_token = create_jwt(user)
    return {
        "access_token": new_token,
        "refresh_token": data.refresh_token,  # Same refresh token returned (vuln #82)
    }


@router.get("/me")
async def get_me(request: Request):
    """Get current user - JWT none algorithm accepted (vuln #72)"""
    auth = request.headers.get("Authorization", "")
    token = auth.replace("Bearer ", "")

    if not token:
        raise HTTPException(status_code=401, detail="No token provided")

    try:
        # Accept none algorithm (vuln #72)
        # Accept any algorithm (vuln #73)
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256", "HS384", "HS512"])
        except jwt.InvalidAlgorithmError:
            # Try without algorithm check (vuln #74)
            payload = jwt.decode(token, options={"verify_signature": False})

        email = payload.get("sub") or payload.get("email")
        user = users_db.get(email, {})
        return {"user": user, "token_payload": payload}
    except jwt.ExpiredSignatureError:
        # No expiry check bypass (vuln #77)
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"], options={"verify_exp": False})
        return {"user": payload, "expired_token": True, "note": "Expired tokens accepted"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/social/google")
async def social_login_google(request: Request):
    """OAuth Google login - redirect URI manipulation (vuln #84, #85)"""
    body = await request.json()
    redirect_uri = body.get("redirect_uri", "http://localhost:3000/callback")
    state = body.get("state", "")  # No state validation (vuln #86)
    code = body.get("code", "")

    # No redirect_uri validation (vuln #85)
    # Attacker can set redirect_uri to their server

    # No state parameter CSRF check (vuln #86)

    # Fake successful OAuth - return token without verification
    # In real app, this would call Google API
    if code:
        # Create account linking - no verification (vuln #94, #95)
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
    """List all users - no auth required (vuln #104, #643)"""
    # Missing function-level authorization
    return {"users": list(users_db.values())}  # Returns ALL user data including PII


@router.post("/bypass")
async def auth_bypass(request: Request):
    """Authentication bypass endpoint (vuln #61)"""
    body = await request.json()
    # Logic flaw - any request with admin=true bypasses auth
    if body.get("admin") or body.get("role") == "admin" or body.get("bypass"):
        user = users_db.get("admin@vulnshop.com")
        return {"token": create_jwt(user), "bypass": True, "user": user}
    raise HTTPException(status_code=401, detail="Unauthorized")
