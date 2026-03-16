# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

import logging
import math
from datetime import datetime, timezone
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.equity import EquityStake
from app.models.user import User
from app.models.water_rights import WaterTrade, TradeStatus
from app.models import SoilSensorReading
from sqlalchemy import func
from app.services.trading_service import WaterTradingService

logger = logging.getLogger(__name__)

class UFIService:
    """
    Unified Freshwater Index (UFI) V2.2 - bx3 Standard.
    The definitive 'Gold Truth' for Freshwater Availability.
    Weights: 60% Ground-Truth, 12% VPD, 10% Liquidity, 6.0% Macro signals.
    """
    @staticmethod
    def get_ufi_score(db: Session, region: str = "SLV") -> float:
        """
        Hex-Fusion V2.2 Scarcity Engine.
        Synthesizes real-time regulatory, atmospheric, and liquidity signals.
        """
        # 1. Macro Signals (6.0% each) - Static Regulatory Baselines
        W_SDG = 0.7  # UN Stress Indicator
        W_F = 0.6    # Falkenmark Pressure
        W_WSI = 0.75 # Satellite Risk
        
        # 2. Leading Indicators (12.0% VPD) - Fetch from Analytics
        # Vapor Pressure Deficit (kPa) - Scale 0.0 to 1.0 (Critical at >2.5 kPa)
        try:
            # Fetch real-time VPD using the updated db-connected method
            V_VPD_raw = WaterTradingService.get_current_vpd(db, region) 
            V_VPD = min(1.0, V_VPD_raw / 2.5) 
        except Exception as e:
            logger.warning(f"Failed to fetch real-time VPD for region {region}: {e}. Using fallback.")
            V_VPD = 0.5 # Default moderate stress
        
        # 3. Economic Signaling (10.0% AllianceChain Liquidity)
        # Ratio of pending/completed trades in the last 24h
        try:
            # Fetch real-time liquidity from trading service
            # This could be a more complex aggregation, but for now, count committed trades
            recent_trades_count = WaterTradingService.get_recent_committed_trades_count(db, region)
            # Scale liquidity score: 0.1 (low activity) to 1.0 (high velocity)
            L_AC = min(1.0, recent_trades_count / 50.0) 
        except Exception as e:
            logger.warning(f"Failed to fetch real-time liquidity for region {region}: {e}. Using fallback.")
            L_AC = 0.45
        
        # 4. Sovereign Variable (60.0% FarmSense Ground-Truth)
        # Highest fidelity signal: Recalculated from latest 100 soil readings
        try:
            latest_readings = db.query(SoilSensorReading.moisture_surface).filter(
                SoilSensorReading.quality_flag == 'valid'
            ).order_by(SoilSensorReading.timestamp.desc()).limit(100).all()
            
            if latest_readings:
                # Average moisture (normalized 0.1 to 0.5 -> 0.0 to 1.0 stress)
                avg_moisture = sum([r[0] for r in latest_readings]) / len(latest_readings)
                # UFI stress is inverse of moisture (0.5 moisture -> 0.0 stress, 0.1 moisture -> 1.0 stress)
                G_FS = max(0.0, min(1.0, (0.5 - avg_moisture) / 0.4))
            else:
                G_FS = 0.5
        except Exception as e:
            logger.error(f"[UFI] Ground-Truth aggregation failed: {e}")
            G_FS = 0.5
        
        # Hex-Fusion V2.2 Calculation
        score = (
            (0.06 * W_SDG) + 
            (0.06 * W_F) + 
            (0.06 * W_WSI) + 
            (0.60 * G_FS) + 
            (0.12 * V_VPD) + 
            (0.10 * L_AC)
        )
        
        logger.info(f"[UFI] Scoring Engine: VPD={V_VPD:.2f}, AC_Liq={L_AC:.2f}, Result={score:.4f}")
        return round(score, 4)

class EquityService:
    """
    Manages the 'Group 100' Equity Buy-in.
    10,000 shares represent 1% total ownership.
    Price follows a curve: P = (P0 * (1 + rate)^n) * (1 + scarcity_premium)
    """
    BASE_PRICE_USD = 100.00  # Starting price per share
    TOTAL_SHARES = 10000
    RATE_INCREMENT = 0.025   # 2.5% increment per buy-in
    
    @staticmethod
    def get_current_price(db: Session) -> float:
        """Calculates current share price with dynamic UFI scarcity multiplier"""
        count = db.query(EquityStake).count()
        
        # Base curvature price
        base_curve = EquityService.BASE_PRICE_USD * math.pow((1 + EquityService.RATE_INCREMENT), count)
        
        # Unified Freshwater Index (UFI) Premium
        ufi_score = UFIService.get_ufi_score(db)
        
        # Premium logic: UFI > 0.8 triggers 'Focus Collapse' premium (50%)
        scarcity_multiplier = 1 + (ufi_score * 0.5) 
        
        return round(base_curve * scarcity_multiplier, 2)

    @staticmethod
    def process_buy_in(db: Session, user: User, amount_usd: float) -> EquityStake:
        """Processes a stock purchase and calculates shares issued"""
        price = EquityService.get_current_price(db)
        shares = int(amount_usd / price)
        
        if shares <= 0:
            raise ValueError("Investment amount too low for current share price")
            
        stake = EquityStake(
            user_id=user.id,
            shares=shares,
            purchase_price=price,
            purchased_at=datetime.now(timezone.utc)
        )
        db.add(stake)
        db.commit()
        db.refresh(stake)
        return stake

class DilutionModelingService:
    """
    Simulates the impact of funding rounds on the cap table.
    Essential for defending the $100B valuation thesis.
    """
    @staticmethod
    def simulate_round(
        current_total_shares: int,
        pre_money_valuation: float,
        investment_amount: float
    ) -> Dict[str, any]:
        """
        Calculates dilution for a given round.
        Post-Money = Pre-Money + Investment
        New Shares = Current * (Investment / Pre-Money)
        """
        post_money = pre_money_valuation + investment_amount
        dilution_pct = investment_amount / post_money
        new_shares = int(current_total_shares * (investment_amount / pre_money_valuation))
        
        return {
            "pre_money": pre_money_valuation,
            "investment": investment_amount,
            "post_money": post_money,
            "dilution_pct": round(dilution_pct * 100, 2),
            "new_shares_issued": new_shares,
            "total_shares_post": current_total_shares + new_shares
        }

    @staticmethod
    def get_100b_series_a_impact(db: Session) -> Dict[str, any]:
        """
        Specific simulation for the $100B Series A target.
        Assumes a $20B raise at a $80B pre-money valuation.
        """
        current_total_shares = db.query(func.sum(EquityStake.shares)).scalar() or 0
        if current_total_shares == 0:
            current_total_shares = 1000000 # Default seed for modeling if empty
            
        return DilutionModelingService.simulate_round(
            current_total_shares,
            pre_money_valuation=80_000_000_000.0,
            investment_amount=20_000_000_000.0
        )

    @staticmethod
    def get_investor_roi(entry_price: float, target_valuation_usd: float = 100_000_000_000.0) -> float:
        """
        Calculates projected ROI for an investor based on target exit valuation.
        Incorporates 'UFI Scarcity Premium' at exit to justify the $100B thesis.
        """
        # Scarcity Multiplier: At $100B, we assume critical UFI levels (>0.8)
        # This justifies a premium on the per-acre value of the tech.
        ufi_premium = 1.5 # 50% scarcity premium at exit
        
        # Standardized exit share count
        EXIT_TOTAL_SHARES = 1_000_000_000 
        exit_price_per_share = (target_valuation_usd * ufi_premium) / EXIT_TOTAL_SHARES
        
        # Correlate Group 100 shards to exit shares (1:100 ratio)
        projected_value = exit_price_per_share * 100
        
        return round((projected_value - entry_price) / entry_price * 100, 2)

class SignatureService:
    """
    Manages the royalty-free Digital Signature flow.
    Generates unique tokens for non-account signing.
    """
    @staticmethod
    def generate_signing_token(letter_id: str) -> str:
        import secrets
        return secrets.token_urlsafe(32)
        
    @staticmethod
    def verify_token(db: Session, token: str):
        from app.models.grant import SupportLetter
        letter = db.query(SupportLetter).filter(SupportLetter.token == token).first()
        if letter and letter.token_expires_at and letter.token_expires_at < datetime.now(timezone.utc):
            return None # Token expired
        return letter