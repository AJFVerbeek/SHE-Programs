"""FastAPI-entrypoint voor de SHE-Programs RI&E-applicatie."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import __version__
from app.config import settings
from app.database import Base, engine
from app.routers import api, web

# Maak de databasetabellen aan bij het opstarten.
# Voor productie is een migratietool (bv. Alembic) aan te raden.
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version=__version__)

_STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(_STATIC_DIR)), name="static")

app.include_router(web.router)
app.include_router(api.router)


@app.get("/health", tags=["systeem"])
def health() -> dict[str, str]:
    """Eenvoudige health-check."""
    return {"status": "ok", "version": __version__}
