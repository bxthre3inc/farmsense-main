import hashlib
import base64
import json
from datetime import datetime, timezone
from typing import Dict, Any
from cryptography.hazmat.primitives.asymmetric import ed25519

def sign_payload(payload: Dict[str, Any], key_seed: bytes = b"farmsense-rss-master-key-v1") -> str:
    """
    Signs a dictionary payload using Ed25519.
    Canonicalizes JSON to ensure stable hashing.
    """
    seed = hashlib.sha256(key_seed).digest()
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
    
    # Canonicalize JSON to ensure stable hashing
    payload_bytes = json.dumps(payload, sort_keys=True).encode('utf-8')
    signature = private_key.sign(payload_bytes)
    
    return f"ed25519:{base64.b64encode(signature).decode('utf-8')}"

def verify_payload(payload: Dict[str, Any], signature_str: str, key_seed: bytes = b"farmsense-rss-master-key-v1") -> bool:
    """
    Verifies an Ed25519 signature on a payload.
    """
    if not signature_str.startswith("ed25519:"):
        return False
        
    try:
        signature = base64.b64decode(signature_str.split(":")[1])
        seed = hashlib.sha256(key_seed).digest()
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
        public_key = private_key.public_key()
        
        payload_bytes = json.dumps(payload, sort_keys=True).encode('utf-8')
        public_key.verify(signature, payload_bytes)
        return True
    except Exception:
        return False
