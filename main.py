import jwt
from fastapi import FastAPI, Response
from pydantic import BaseModel

app = FastAPI(title="OIDC Token Verification Service")

# ---- Assigned values ----
ISSUER = "https://idp.exam.local"
AUDIENCE = "tds-e51o68cq.apps.exam.local"

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2okOHspNjgA+2rTLbeuY
cxiP/hG8C6Sb9iwg3yiLAA4HCnpITcbWCSelbvbYGuc3EbNy4xFyf5Cbj5DHJMID
EkryOgyd2giIIIBOUBj8S63uGcnRpOBh9NFatfNwheKuzsPuVN1du6A9cNteNpXc
WyJjG2axVfmq7i6SuKr1JoWYG7xTTAvKPujSl4OtsQfO3h5NepzdfXpr28oNnzfW
ed+zc1R6BcmNNo/WVfJ4xyCLSf0BCOgdTgW6PdaChd119VDetJZVEgC5tkyvXsfI
SI6iyrYbKR0NEBSqq4XkadEjsCs4F1RncsS4L1gniT7G1kL9Mce3b0wGLs9/7ZIX
dQIDAQAB
-----END PUBLIC KEY-----"""


class TokenRequest(BaseModel):
    token: str


@app.post("/verify")
def verify(req: TokenRequest, response: Response):
    try:
        claims = jwt.decode(
            req.token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            issuer=ISSUER,
            audience=AUDIENCE,
            options={
                "require": ["exp", "iss", "aud"],
                "verify_signature": True,
                "verify_exp": True,
                "verify_iss": True,
                "verify_aud": True,
            },
        )
    except jwt.PyJWTError as e:
        response.status_code = 401
        return {"valid": False, "_debug_error": str(e), "_debug_type": type(e).__name__}

    response.status_code = 200
    return {
        "valid": True,
        "email": claims.get("email"),
        "sub": claims.get("sub"),
        "aud": claims.get("aud"),
    }


@app.get("/")
def root():
    return {"status": "ok", "service": "OIDC Token Verification Service"}


@app.post("/debug-decode")
def debug_decode(req: TokenRequest):
    """TEMPORARY debug endpoint: shows raw unverified claims + header."""
    import hashlib
    header = jwt.get_unverified_header(req.token)
    claims = jwt.decode(req.token, options={"verify_signature": False})
    key_hash = hashlib.sha256(PUBLIC_KEY.encode()).hexdigest()
    return {
        "header": header,
        "claims": claims,
        "expected_issuer": ISSUER,
        "expected_audience": AUDIENCE,
        "public_key_sha256": key_hash,
    }
