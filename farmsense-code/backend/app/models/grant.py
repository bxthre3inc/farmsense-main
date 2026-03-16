# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean, Float, Integer, Enum as sqlalchemy_enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
import enum
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from .base import Base

class LetterStatus(str, enum.Enum):
    PENDING = "pending"
    SIGNED = "signed"
    VERIFIED = "verified"
    REJECTED = "rejected"

class SupportLetter(Base):
    __tablename__ = 'support_letters'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    grant_id = Column(String(50), nullable=False, index=True)
    sender_name = Column(String(100), nullable=False)
    sender_email = Column(String(255), nullable=False, index=True)
    sender_organization = Column(String(200))
    content = Column(Text, nullable=False)
    status = Column(sqlalchemy_enum(LetterStatus), default=LetterStatus.PENDING)
    signature_data = Column(Text) # Base64 or digital signature hash
    is_digital = Column(Boolean, default=True)
    file_path = Column(String(512)) # For manual uploads
    token = Column(String(128), unique=True, index=True) # Public signing token
    token_expires_at = Column(DateTime)
    signed_at = Column(DateTime)
    verified_at = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# Pydantic Schemas
class SupportLetterBase(BaseModel):
    grant_id: str
    sender_name: str
    sender_email: EmailStr
    sender_organization: Optional[str] = None
    content: str

class SupportLetterCreate(SupportLetterBase):
    pass

class SupportLetterSign(BaseModel):
    signature_data: str

class SupportLetterRead(SupportLetterBase):
    id: uuid.UUID
    status: LetterStatus
    signed_at: Optional[datetime] = None
    verified_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True