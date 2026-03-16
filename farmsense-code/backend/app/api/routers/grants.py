# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.core.database import get_db
from app.api.dependencies import get_current_user, RequireRole
from app.models.user import User, UserRole

from app.models.grant import SupportLetter, LetterStatus, SupportLetterCreate, SupportLetterRead, SupportLetterSign
from app.services.equity_service import SignatureService

router = APIRouter()

@router.get("/support-letters/{grant_id}", response_model=List[SupportLetterRead], tags=["Grants"])
def list_support_letters(grant_id: str, db: Session = Depends(get_db)):
    """List all support letters for a specific grant"""
    return db.query(SupportLetter).filter(SupportLetter.grant_id == grant_id).all()

@router.post("/support-letters/{grant_id}/request", response_model=SupportLetterRead, tags=["Grants"])
def request_support_letter(
    grant_id: str, 
    letter_in: SupportLetterCreate, 
    db: Session = Depends(get_db)
):
    """Request a new support letter (reviewer uploads unsigned content)"""
    new_letter = SupportLetter(
        grant_id=grant_id,
        signer_email=letter_in.signer_email,
        md_content=letter_in.md_content,
        status=LetterStatus.PENDING
    )
    db.add(new_letter)
    db.commit()
    db.refresh(new_letter)
    
    # In reality, trigger email to letter_in.signer_email with a signing link containing the ID
    return new_letter

@router.post("/support-letters/verify/{letter_id}", tags=["Grants"])
def verify_support_letter(
    letter_id: uuid.UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Admin/Reviewer endpoint to verify a signed letter"""
    letter = db.query(SupportLetter).filter(SupportLetter.id == letter_id).first()
    if not letter:
        raise HTTPException(status_code=404, detail="Letter not found")
        
    sig_service = SignatureService()
    public_key = sig_service.get_public_key_for_user(letter.signer_email)
    
    if not public_key:
        return {"verified": False, "reason": "No public key registered for this email"}
        
    is_valid = sig_service.verify_signature(
        letter.signature_payload, 
        letter.signature_hash, 
        public_key
    )
    
    if is_valid:
        letter.status = LetterStatus.VERIFIED
        db.commit()
        
    return {"verified": is_valid}

@router.post("/investor/buy-in", tags=["Investor"])
def process_investor_buy_in(
    amount: float,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """Processes a stock buy-in for a logged-in investor"""
    from app.services.equity_service import EquityService
    
    try:
        stake = EquityService.process_buy_in(db, user, amount)
        # In MVP, tier is a string. Update to Enum later if needed.
        user.tier = "ENTERPRISE"
        db.commit()
        return {
            "status": "success", 
            "message": f"Successfully processed ${amount} buy-in. Issued {stake.shares} shares.",
            "shares_issued": stake.shares,
            "purchase_price": stake.purchase_price
        }
    except Exception as e:
        from fastapi import HTTPException
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))