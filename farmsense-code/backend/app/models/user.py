# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from sqlalchemy import Column, String, Enum, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum
from .base import Base

class SubscriptionTier(str, enum.Enum):
    FREE = "FREE"             # 50 meters
    BASIC = "BASIC"           # 20 meters
    PRO = "PRO"               # 10 meters
    ENTERPRISE = "ENTERPRISE" # 1 meter + Drone

class UserRole(str, enum.Enum):
    FARMER = "FARMER"
    AUDITOR = "AUDITOR"
    ADMIN = "ADMIN"
    RESEARCHER = "RESEARCHER"
    INVESTOR = "INVESTOR"
    REVIEWER = "REVIEWER"
    PARTNER = "PARTNER"
    REGULATOR = "REGULATOR"
    INTERNAL = "INTERNAL"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    organization = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    api_key = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.FARMER, nullable=False)
    is_active = Column(Boolean, default=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)