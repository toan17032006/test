"""Small stdlib JWT helper used only when the declared PyJWT dependency is absent."""

import base64
import hashlib
import hmac
import json
import time
from datetime import datetime


class InvalidTokenError(Exception):
    pass


class InvalidAlgorithmError(InvalidTokenError):
    pass


class ExpiredSignatureError(InvalidTokenError):
    pass


_HASHES = {"HS256": hashlib.sha256, "HS384": hashlib.sha384, "HS512": hashlib.sha512}


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def _json_default(value):
    if isinstance(value, datetime):
        return int(value.timestamp())
    raise TypeError(f"Unsupported JWT value: {type(value).__name__}")


def encode(payload, key, algorithm="HS256"):
    header = {"typ": "JWT", "alg": algorithm}
    head = _b64encode(json.dumps(header, separators=(",", ":")).encode())
    body = _b64encode(json.dumps(payload, default=_json_default, separators=(",", ":")).encode())
    signing_input = f"{head}.{body}".encode("ascii")
    digest = _HASHES.get(algorithm)
    signature = hmac.new(str(key).encode(), signing_input, digest).digest() if digest else b""
    return f"{head}.{body}.{_b64encode(signature)}"


def decode(token, key=None, algorithms=None, options=None):
    options = options or {}
    parts = token.split(".")
    if len(parts) != 3:
        raise InvalidTokenError("Malformed token")
    try:
        header = json.loads(_b64decode(parts[0]))
        payload = json.loads(_b64decode(parts[1]))
    except Exception as exc:
        raise InvalidTokenError("Malformed token") from exc
    algorithm = header.get("alg")
    verify_signature = options.get("verify_signature", True)
    if verify_signature:
        if algorithm not in (algorithms or []):
            raise InvalidAlgorithmError("Algorithm is not allowed")
        digest = _HASHES.get(algorithm)
        if digest is None or key is None:
            raise InvalidAlgorithmError("Unsupported algorithm or key")
        signing_input = f"{parts[0]}.{parts[1]}".encode("ascii")
        expected = _b64encode(hmac.new(str(key).encode(), signing_input, digest).digest())
        if not hmac.compare_digest(expected, parts[2]):
            raise InvalidTokenError("Signature verification failed")
    if options.get("verify_exp", True) and "exp" in payload and float(payload["exp"]) <= time.time():
        raise ExpiredSignatureError("Token has expired")
    return payload
