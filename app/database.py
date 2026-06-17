"""Database-configuratie: engine, sessie en de declaratieve basisklasse."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

# Voor SQLite is `check_same_thread=False` nodig bij gebruik met FastAPI.
_connect_args = (
    {"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {}
)

engine = create_engine(settings.database_url, connect_args=_connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Declaratieve basisklasse voor alle ORM-modellen."""


def get_db() -> Generator[Session, None, None]:
    """FastAPI-dependency die per request een databasesessie levert."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
