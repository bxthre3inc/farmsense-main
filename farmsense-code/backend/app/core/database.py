# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

"""
Database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from typing import Generator
import os

# Database URLs from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://farmsense_user:changeme@localhost:5432/farmsense"
)

TIMESCALE_URL = os.getenv(
    "TIMESCALE_URL",
    "postgresql://timescale_user:changeme@localhost:5433/farmsense_timeseries"
)

MAP_DATABASE_URL = os.getenv(
    "MAP_DATABASE_URL",
    "postgresql://map_user:changeme@localhost:5432/farmsense_map"
)

# SQLAlchemy engine configuration
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

# TimescaleDB engine for time-series data
timescale_engine = create_engine(
    TIMESCALE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=False
)

# Map database engine
map_engine = create_engine(
    MAP_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=False
)

# Session factories
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TimescaleSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=timescale_engine)
MapSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=map_engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database sessions
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_timescale_db() -> Generator[Session, None, None]:
    """Database dependency for time-series data"""
    db = TimescaleSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_map_db() -> Generator[Session, None, None]:
    """Database dependency for Map/Tile data"""
    db = MapSessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    from app.models import sensor_data
    
    # Create all tables
    sensor_data.Base.metadata.create_all(bind=engine)
    
    # Create PostGIS extension
    with engine.connect() as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    
    print("Database initialized successfully")


if __name__ == "__main__":
    init_db()