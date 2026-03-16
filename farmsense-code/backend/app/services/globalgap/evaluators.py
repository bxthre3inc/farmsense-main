# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from .models import GAP_FieldInputs, ControlPointResult
from .constants import ControlPointID, CONTROL_POINT_DESCRIPTIONS, NCLevel

class GAPEvaluator:
    @staticmethod
    def score_to_level(
        score: float,
        critical_threshold: float,
        major_threshold: float,
        minor_threshold: float,
    ) -> NCLevel:
        if score <= critical_threshold:
            return NCLevel.CRITICAL_NC
        if score < major_threshold:
            return NCLevel.MAJOR_NC
        if score < minor_threshold:
            return NCLevel.MINOR_NC
        return NCLevel.PASS

    @classmethod
    def evaluate_af12(cls, i: GAP_FieldInputs) -> ControlPointResult:
        score = 0.0
        evidence, findings, actions = [], [], []

        if i.site_risk_assessment_date:
            score += 0.5
            evidence.append(f"Site risk assessment on file: {i.site_risk_assessment_date}")
        else:
            findings.append("No site risk assessment date recorded.")
            actions.append("Complete a documented site risk assessment before next audit.")

        if i.previous_land_use_documented:
            score += 0.3
            evidence.append("Previous land use history documented.")
        else:
            findings.append("Previous land use history not documented.")
            actions.append("Document farm history for at least 5 years prior to current use.")

        if i.restricted_substances_audit:
            score += 0.2
            evidence.append("Restricted substance audit completed.")
        else:
            findings.append("Restricted substance audit not completed.")
            actions.append("Conduct and document a restricted substance soil/water audit.")

        level = cls.score_to_level(score, critical_threshold=0.0, major_threshold=0.5, minor_threshold=0.8)
        return ControlPointResult(ControlPointID.AF_1_2.value, CONTROL_POINT_DESCRIPTIONS[ControlPointID.AF_1_2], round(score, 3), level, evidence, findings, actions)

    @classmethod
    def evaluate_cb52(cls, i: GAP_FieldInputs) -> ControlPointResult:
        score = 0.0
        evidence, findings, actions = [], [], []

        if i.water_source_type in ["groundwater", "surface", "municipal", "recycled"]:
            score += 0.5
            evidence.append(f"Water source type identified: {i.water_source_type}")
        else:
            findings.append(f"Water source type '{i.water_source_type}' not recognized.")

        if i.water_source_documented:
            score += 0.5
            evidence.append("Water source permit/documentation on file.")
        else:
            findings.append("Water source not formally documented (permit, well log, or water right).")
            actions.append("Obtain and file water right documentation or well completion report.")

        level = cls.score_to_level(score, critical_threshold=0.0, major_threshold=0.5, minor_threshold=0.9)
        return ControlPointResult(ControlPointID.CB_5_2.value, CONTROL_POINT_DESCRIPTIONS[ControlPointID.CB_5_2], round(score, 3), level, evidence, findings, actions)

    @classmethod
    def evaluate_cb53(cls, i: GAP_FieldInputs) -> ControlPointResult:
        score = 0.0
        evidence, findings, actions = [], [], []

        RECOGNIZED_METHODS = {"drip", "sprinkler", "flood", "subsurface", "pivot"}
        if i.application_method.lower() in RECOGNIZED_METHODS:
            score += 0.6
            evidence.append(f"Application method specified: {i.application_method}")
        else:
            findings.append(f"Application method '{i.application_method}' not in recognized list.")

        if i.application_method_documented:
            score += 0.4
            evidence.append("Application method formally documented.")
        else:
            findings.append("Application method not documented in farm records.")
            actions.append("Document irrigation application method, frequency, and seasonal schedule.")

        level = cls.score_to_level(score, critical_threshold=0.0, major_threshold=0.4, minor_threshold=0.8)
        return ControlPointResult(ControlPointID.CB_5_3.value, CONTROL_POINT_DESCRIPTIONS[ControlPointID.CB_5_3], round(score, 3), level, evidence, findings, actions)

    @classmethod
    def evaluate_cb55(cls, i: GAP_FieldInputs) -> ControlPointResult:
        score = 0.0
        evidence, findings, actions = [], [], []

        if i.ec_within_threshold:
            score += 0.3
            evidence.append(f"Mean EC {i.avg_ec_us_cm:.0f} µS/cm — within GLOBALG.A.P. threshold (<2500).")
        else:
            findings.append(f"EC {i.avg_ec_us_cm:.0f} µS/cm exceeds GLOBALG.A.P. threshold of 2500 µS/cm.")
            actions.append("Investigate high EC source; document mitigation (dilution, source change).")

        if i.ph_within_threshold:
            score += 0.3
            evidence.append(f"pH range {i.min_ph:.1f}–{i.max_ph:.1f} — within acceptable range (5.5–8.5).")
        else:
            findings.append(f"pH range {i.min_ph:.1f}–{i.max_ph:.1f} outside acceptable range.")
            actions.append("Adjust irrigation water pH or document treatment protocol.")

        if i.microbiological_test_conducted:
            score += 0.4
            evidence.append("Microbiological water quality test conducted this season.")
        else:
            findings.append("No microbiological test on irrigation water found for this period.")
            actions.append("Conduct and file annual microbiological water quality test (E. coli, generic coliform).")

        level = cls.score_to_level(score, critical_threshold=0.2, major_threshold=0.5, minor_threshold=0.8)
        return ControlPointResult(ControlPointID.CB_5_5.value, CONTROL_POINT_DESCRIPTIONS[ControlPointID.CB_5_5], round(score, 3), level, evidence, findings, actions)

    @classmethod
    def evaluate_fv51(cls, i: GAP_FieldInputs) -> ControlPointResult:
        score = 0.0
        evidence, findings, actions = [], [], []

        if i.documented_efficiency_target:
            score += 0.3
            evidence.append(f"Written water efficiency target documented: {i.efficiency_target_pct:.1f}% reduction.")
        else:
            findings.append("No documented water efficiency target.")
            actions.append("Establish a written seasonal water efficiency target (e.g., 10% vs. prior season).")

        if i.actual_efficiency_gain_pct >= i.efficiency_target_pct and i.efficiency_target_pct > 0:
            score += 0.5
            evidence.append(f"Efficiency target met: {i.actual_efficiency_gain_pct:.1f}% actual vs {i.efficiency_target_pct:.1f}% target.")
        elif i.actual_efficiency_gain_pct > 0:
            score += 0.25
            findings.append(f"Efficiency target partially met: {i.actual_efficiency_gain_pct:.1f}% actual vs {i.efficiency_target_pct:.1f}% target.")
            actions.append("Review irrigation scheduling; consider variable-rate technology or SPAC-based algorithms.")
        else:
            findings.append("No measurable water efficiency improvement recorded this period.")

        yoy_delta = i.prev_season_water_applied_m3 - i.season_water_applied_m3
        if yoy_delta > 0:
            pct = yoy_delta / i.prev_season_water_applied_m3 * 100 if i.prev_season_water_applied_m3 > 0 else 0.0
            score += 0.2
            evidence.append(f"Year-over-year reduction: {pct:.1f}% ({yoy_delta:.0f} m³ saved).")
        else:
            findings.append("Water use did not decrease vs prior season.")

        level = cls.score_to_level(score, critical_threshold=0.0, major_threshold=0.3, minor_threshold=0.7)
        return ControlPointResult(ControlPointID.FV_5_1.value, CONTROL_POINT_DESCRIPTIONS[ControlPointID.FV_5_1], round(score, 3), level, evidence, findings, actions)

    @classmethod
    def evaluate_ag52(cls, i: GAP_FieldInputs) -> ControlPointResult:
        score = 0.0
        evidence, findings, actions = [], [], []

        if i.calibrated_meter_installed:
            score += 0.4
            evidence.append("Calibrated volumetric water meter installed.")
            if i.meter_last_calibration_date:
                evidence.append(f"Last calibration: {i.meter_last_calibration_date}")
        else:
            findings.append("No calibrated water meter installed.")
            actions.append("Install and calibrate a volumetric water meter. Annual calibration required.")

        if i.monthly_meter_logs:
            score += 0.4
            evidence.append("Monthly meter readings logged for full reporting period.")
        else:
            findings.append("Monthly meter logs incomplete; fewer than 12 entries in reporting period.")
            actions.append("Implement regular monthly meter reading protocol and record in farm log.")

        if i.total_metered_volume_m3 > 0:
            score += 0.2
            evidence.append(f"Total metered volume: {i.total_metered_volume_m3:,.1f} m³ for reporting period.")

        level = cls.score_to_level(score, critical_threshold=0.0, major_threshold=0.4, minor_threshold=0.8)
        return ControlPointResult(ControlPointID.AG5_2.value, CONTROL_POINT_DESCRIPTIONS[ControlPointID.AG5_2], round(score, 3), level, evidence, findings, actions)