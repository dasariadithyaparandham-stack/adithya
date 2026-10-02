import base64
import hashlib
import hmac
import json
import secrets
import time

from app.config import settings


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 310_000)
    return f'{salt.hex()}${digest.hex()}'


def verify_password(password: str, password_hash: str) -> bool:
    try:
        salt_hex, digest_hex = password_hash.split('$', 1)
        digest = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt_hex), 310_000)
        return hmac.compare_digest(digest.hex(), digest_hex)
    except (ValueError, TypeError):
        return False


def create_access_token(user_id: int) -> str:
    payload = json.dumps({'sub': user_id, 'exp': int(time.time()) + 60 * 60 * 24 * 7}, separators=(',', ':'))
    encoded_payload = base64.urlsafe_b64encode(payload.encode()).decode().rstrip('=')
    signature = hmac.new(settings.SECRET_KEY.encode(), encoded_payload.encode(), hashlib.sha256).hexdigest()
    return f'{encoded_payload}.{signature}'


def decode_access_token(token: str) -> int | None:
    try:
        encoded_payload, supplied_signature = token.split('.', 1)
        expected_signature = hmac.new(settings.SECRET_KEY.encode(), encoded_payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(supplied_signature, expected_signature):
            return None
        payload = base64.urlsafe_b64decode(encoded_payload + '=' * (-len(encoded_payload) % 4))
        claims = json.loads(payload)
        if claims.get('exp', 0) <= int(time.time()):
            return None
        return int(claims['sub'])
    except (ValueError, TypeError, KeyError, json.JSONDecodeError):
        return None