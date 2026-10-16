import os
import httpx
from typing import Annotated, List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import get_db, engine, Base
from app.models import Videogame
from app.schemas import VideogameCreate, VideogameUpdate, VideogameResponse

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# Create tables automatically if not present
Base.metadata.create_all(bind=engine)

KC_INTERNAL = os.getenv("KEYCLOAK_INTERNAL", "http://keycloak:8080")
KC_PUBLIC = os.getenv("KEYCLOAK_PUBLIC", "http://localhost:8081")
REALM = os.getenv("KEYCLOAK_REALM", "cybersecurity")
CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "fastapi-api")
ISSUER = f"{KC_PUBLIC}/realms/{REALM}"
JWKS_URL = f"{KC_INTERNAL}/realms/{REALM}/protocol/openid-connect/certs"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{ISSUER}/protocol/openid-connect/auth",
    tokenUrl=f"{ISSUER}/protocol/openid-connect/token",
    scopes={"openid": "OpenID Connect identity"},
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse



app = FastAPI(
    title="Videogames API - LDAP + Keycloak JWT Service",
    version="1.0.0",
    description="...",
    docs_url="/docs" if ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if ENVIRONMENT != "production" else None,
    openapi_url="/openapi.json" if ENVIRONMENT != "production" else None,
)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "font-src 'self' https://fonts.googleapis.com https://fonts.gstatic.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com"
        )
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        return response

app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "service": "videogames-api"}

async def current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(JWKS_URL, timeout=5)
            res.raise_for_status()
            jwks = res.json()
        header = jwt.get_unverified_header(token)
        key = next((k for k in jwks.get("keys", []) if k.get("kid") == header.get("kid")), None)
        if not key:
            raise HTTPException(status_code=401, detail="Signing key not found")
        
        # Decode & verify JWT token
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=CLIENT_ID,
            issuer=ISSUER
        )
        return payload
    except (JWTError, httpx.HTTPError, StopIteration) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid access token: {e}",
            headers={"WWW-Authenticate": "Bearer"}
        )

@app.get("/api/videogames", response_model=List[VideogameResponse], tags=["Videogames"])
def list_videogames(
    user: Annotated[dict, Depends(current_user)],
    db: Session = Depends(get_db)
):
    """Retrieve all videogames from SQL Database (Requires valid LDAP/Keycloak JWT)."""
    return db.query(Videogame).all()

@app.get("/api/videogames/{game_id}", response_model=VideogameResponse, tags=["Videogames"])
def get_videogame(
    game_id: int,
    user: Annotated[dict, Depends(current_user)],
    db: Session = Depends(get_db)
):
    """Get a single videogame by ID from SQL Database."""
    game = db.query(Videogame).filter(Videogame.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Videogame not found")
    return game

@app.post("/api/videogames", response_model=VideogameResponse, status_code=status.HTTP_201_CREATED, tags=["Videogames"])
def create_videogame(
    game_data: VideogameCreate,
    user: Annotated[dict, Depends(current_user)],
    db: Session = Depends(get_db)
):
    """Create a new videogame entry in SQL Database."""
    game = Videogame(**game_data.model_dump())
    db.add(game)
    db.commit()
    db.refresh(game)
    return game

@app.put("/api/videogames/{game_id}", response_model=VideogameResponse, tags=["Videogames"])
def update_videogame(
    game_id: int,
    game_data: VideogameUpdate,
    user: Annotated[dict, Depends(current_user)],
    db: Session = Depends(get_db)
):
    """Update existing videogame in SQL Database."""
    game = db.query(Videogame).filter(Videogame.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Videogame not found")
    
    update_data = game_data.model_dump(exclude_unset=True)
    for key, val in update_data.items():
        setattr(game, key, val)
        
    db.commit()
    db.refresh(game)
    return game

@app.delete("/api/videogames/{game_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Videogames"])
def delete_videogame(
    game_id: int,
    user: Annotated[dict, Depends(current_user)],
    db: Session = Depends(get_db)
):
    """Delete a videogame entry from SQL Database."""
    game = db.query(Videogame).filter(Videogame.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Videogame not found")
    db.delete(game)
    db.commit()
    return None

# Serve React SPA static files if compiled dist exists in app/static
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    assets_dir = os.path.join(static_dir, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="static_assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path == "openapi.json" or full_path == "health":
            raise HTTPException(status_code=404, detail="Not Found")
        file_path = os.path.join(static_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        index_file = os.path.join(static_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        raise HTTPException(status_code=404, detail="Static index.html not found")
