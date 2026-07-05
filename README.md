# OIDC Token Verification Service

FastAPI service exposing `POST /verify` that validates RS256 JWTs against:
- Signature (RS256, using the IdP's public key embedded in `main.py`)
- Issuer (`iss` == `https://idp.exam.local`)
- Audience (`aud` == `tds-e51o68cq.apps.exam.local`)
- Expiry (`exp` in the future)

Returns `200 {"valid": true, "email":..., "sub":..., "aud":...}` on success,
`401 {"valid": false}` on any failure.

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Test:
```bash
curl -X POST http://localhost:8000/verify \
  -H "Content-Type: application/json" \
  -d '{"token": "<JWT>"}'
```

## Deploy (pick any public host)

### Option A: Render.com (free, easiest)
1. Push this folder to a new GitHub repo.
2. On render.com -> New -> Web Service -> connect the repo.
3. Environment: Docker (it will auto-detect the Dockerfile), or:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Deploy. Your endpoint will be `https://<your-app>.onrender.com/verify`.

### Option B: Railway.app
1. `railway init` in this folder, then `railway up`.
2. Railway auto-detects the Dockerfile and exposes a public URL.
3. Endpoint: `https://<your-app>.up.railway.app/verify`.

### Option C: Fly.io
```bash
fly launch   # accept defaults, it detects the Dockerfile
fly deploy
```
Endpoint: `https://<your-app>.fly.dev/verify`.

### Option D: Any VM / Docker host
```bash
docker build -t oidc-verify .
docker run -p 8000:8000 oidc-verify
```
Put it behind a reverse proxy / public DNS name, then use
`https://your-domain/verify`.

Once deployed, paste the full URL (e.g. `https://my-app.onrender.com/verify`)
into the grader's "Your deployed /verify endpoint URL" field.
