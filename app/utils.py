import hmac, hashlib, os

def verify_signature(payload: bytes, sig: str) -> bool:
    secret = os.getenv("FW_WEBHOOK_SECRET").encode()
    mac = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, sig)
