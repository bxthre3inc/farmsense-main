# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

"""
FastAPI Backend - FarmSense API Entrypoint
"""
import uvicorn
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware

from app.api.dependencies import get_db, get_current_user
from app.models.base import Base
from app.core.database import engine
from app.api.integration import router as integration_router
from app.api import tiles
from app.core.websocket import manager

from app.api.routers import hardware, users, metrics, grants, analytics, compliance, trading, federated, auth, fields

# Skip auto-create in production - use Alembic migrations
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FarmSense API",
    description="Deterministic Agricultural Intelligence Platform. No Black Box AI.",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("FarmSense API starting up...")


# === Include APIRouters ===
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(hardware.router, prefix="/api/v1/hardware", tags=["Hardware Ingestion"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Admin User Management"])
app.include_router(metrics.router, prefix="/api/v1/metrics", tags=["Stakeholders and Metrics"])
app.include_router(grants.router, prefix="/api/v1/grants", tags=["Grants & Investment"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Geospatial Analytics"])
app.include_router(compliance.router, prefix="/api/v1/compliance", tags=["Compliance Reporting"])
app.include_router(trading.router, prefix="/api/v1/trade", tags=["Water Rights Trading"])
app.include_router(federated.router, prefix="/api/v1/federated", tags=["Federated Data Fabric"])
app.include_router(fields.router, prefix="/api/v1/fields", tags=["Field Management & Boundaries"])

# Keep legacy integration and tile routers
app.include_router(integration_router, prefix="/api/v1", tags=["Integration"])
app.include_router(tiles.router, prefix="/api/v1", tags=["tiles"])

# === Global WebSocket Real-time Endpoint ===
# IMPORTANT: JWT_SECRET must match the NEXTAUTH_SECRET to validate tokens from the frontend
JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET environment variable must be set - no fallback allowed")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(None)):
    """
    Handles realtime dashboard updates via WebSockets.
    Authentication is handled via the query token.
    """
    import jwt
    from fastapi import status
    
    # Verify JWT implicitly before accepting to protect socket resources
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
        
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Token missing subject")
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket)
    try:
        while True:
            # FarmSense dashboard uses one-way sockets for downstream data currently
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# === Base Routes ===

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "system": "FarmSense Core Engine",
        "documentation": "/docs"
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for load balancer"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)