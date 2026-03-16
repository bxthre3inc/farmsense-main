# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

import math
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PricingService:
    """
    Core pricing engine for FarmSense Software-as-a-Service.
    Implements a tiered discount structure based on the number of active fields.
    """
    
    BASE_PRICE_PER_FIELD = {
        "COMPLIANCE": 0.0,       # Free (Grant Subsidized)
        "STANDARD": 150.0,       # Monthly base
        "ENTERPRISE": 500.0      # Monthly minimum (Master RSS Grid)
    }

    @staticmethod
    def calculate_discount_pct(num_fields: int) -> float:
        """
        Calculates the cumulative discount percentage based on volume.
        
        Logic:
        - 1 Field: 0.0% (Standard Rate)
        - 2+ Fields: Starts at 5% discount, grows by 2.5% per field until 15% (at Field 6)
        - Fields 7-16: Increases by 1% for every 2 fields until 20% (at Field 16)
        - Fields 17-66: Increases by 1% for every 10 fields until 25% (at Field 66)
        - Max: 25%
        """
        if num_fields <= 1:
            return 0.0
            
        discount = 0.0
        
        # Tier 1: 5% to 15% (Steps of 2.5%)
        if num_fields >= 2:
            # Field 2 is 5%, Field 3 is 7.5%...
            t1_steps = min(num_fields - 1, 5) # Max 5 steps (Field 2 to 6)
            discount = 5.0 + (t1_steps - 1) * 2.5
            
        # Tier 2: 15% to 20% (Steps of 1% per 2 fields)
        if num_fields > 6:
            t2_fields = min(num_fields - 6, 10) # Max 10 fields (7 to 16)
            discount += (t2_fields // 2) * 1.0 # 1% for every 2
            
        # Tier 3: 20% to 25% (Steps of 1% per 10 fields)
        if num_fields > 16:
            t3_fields = min(num_fields - 16, 50) # Max 50 fields (17 to 66)
            discount += (t3_fields // 10) * 1.0 # 1% for every 10
            
        return min(discount, 25.0)

    @staticmethod
    def get_subscription_estimate(num_fields: int, tier: str = "STANDARD") -> Dict[str, Any]:
        """
        Generates a monthly billing estimate for a grower.
        """
        unit_price = PricingService.BASE_PRICE_PER_FIELD.get(tier.upper(), 150.0)
        discount_pct = PricingService.calculate_discount_pct(num_fields)
        
        raw_total = num_fields * unit_price
        discount_amount = raw_total * (discount_pct / 100.0)
        final_total = raw_total - discount_amount
        
        return {
            "tier": tier.upper(),
            "num_fields": num_fields,
            "unit_price": unit_price,
            "discount_pct": f"{discount_pct}%",
            "monthly_total": round(final_total, 2),
            "effective_price_per_field": round(final_total / num_fields, 2) if num_fields > 0 else 0
        }