# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

import hashlib
import uuid
from datetime import datetime, timezone
from .models import GAP_FieldInputs, GAP_Report, ControlPointResult
from .constants import ControlPointID, CONTROL_POINT_WEIGHTS, NCLevel
from .evaluators import GAPEvaluator

class GAPComplianceEngine:
    """Generates GLOBALG.A.P. IFA v6 compliance reports from FarmSense data."""

    def generate(self, inputs: GAP_FieldInputs) -> GAP_Report:
        now = datetime.now(timezone.utc).isoformat()
        report_id = f"GAP-{inputs.field_id[:8].upper()}-{uuid.uuid4().hex[:6].upper()}"

        results: list[ControlPointResult] = []

        # ── AF 1.2 — Site History ──────────────────────────────────────
        results.append(GAPEvaluator.evaluate_af12(inputs))

        # ── CB 5.2 — Water Source ──────────────────────────────────────
        results.append(GAPEvaluator.evaluate_cb52(inputs))

        # ── CB 5.3 — Application Method ───────────────────────────────
        results.append(GAPEvaluator.evaluate_cb53(inputs))

        # ── CB 5.5 — Water Quality ────────────────────────────────────
        results.append(GAPEvaluator.evaluate_cb55(inputs))

        # ── FV 5.1 — Efficiency ───────────────────────────────────────
        results.append(GAPEvaluator.evaluate_fv51(inputs))

        # ── AG 5.2 — Metering ─────────────────────────────────────────
        results.append(GAPEvaluator.evaluate_ag52(inputs))

        # ── Overall Score ──────────────────────────────────────────────
        overall_score = sum(
            r.score * CONTROL_POINT_WEIGHTS.get(ControlPointID(r.control_point_id), 0.0)
            for r in results
        )

        # Determine overall certification status
        levels = [r.level for r in results]
        if NCLevel.CRITICAL_NC in levels:
            cert_status = NCLevel.CRITICAL_NC
        elif NCLevel.MAJOR_NC in levels:
            cert_status = NCLevel.MAJOR_NC
        elif NCLevel.MINOR_NC in levels:
            cert_status = NCLevel.MINOR_NC
        else:
            cert_status = NCLevel.PASS

        # ── Narrative + Markdown ───────────────────────────────────────
        narrative = self._build_narrative(inputs, results, overall_score, cert_status)
        markdown  = self._build_markdown(inputs, results, overall_score, cert_status, report_id, now)

        # ── Verifiable Hash ────────────────────────────────────────────
        hash_input = f"{report_id}:{inputs.field_id}:{inputs.report_period_start}:{inputs.report_period_end}:{overall_score:.4f}:{cert_status.value}"
        vhash = hashlib.sha256(hash_input.encode()).hexdigest()

        return GAP_Report(
            report_id=report_id,
            field_id=inputs.field_id,
            field_name=inputs.field_name,
            farm_name=inputs.farm_name,
            grower_id=inputs.grower_id,
            period_start=inputs.report_period_start,
            period_end=inputs.report_period_end,
            generated_at=now,
            control_points=results,
            overall_score=round(overall_score, 4),
            certification_status=cert_status,
            summary_narrative=narrative,
            markdown_report=markdown,
            verifiable_hash=vhash,
        )

    @staticmethod
    def _build_narrative(
        inputs: GAP_FieldInputs,
        results: list[ControlPointResult],
        score: float,
        status: NCLevel,
    ) -> str:
        pass_count  = sum(1 for r in results if r.level == NCLevel.PASS)
        minor_count = sum(1 for r in results if r.level == NCLevel.MINOR_NC)
        major_count = sum(1 for r in results if r.level == NCLevel.MAJOR_NC)
        crit_count  = sum(1 for r in results if r.level == NCLevel.CRITICAL_NC)

        status_label  = {
            NCLevel.PASS:        "PASS — no non-conformances detected",
            NCLevel.MINOR_NC:    "MINOR NON-CONFORMANCE(S) — corrective actions required",
            NCLevel.MAJOR_NC:    "MAJOR NON-CONFORMANCE(S) — suspension risk unless corrected",
            NCLevel.CRITICAL_NC: "CRITICAL NON-CONFORMANCE — certification suspended",
        }[status]

        return (
            f"GLOBALG.A.P. IFA v6 compliance evaluation for {inputs.field_name} "
            f"({inputs.farm_name}) covering {inputs.report_period_start} to {inputs.report_period_end}. "
            f"Overall score: {score * 100:.1f}/100. Status: {status_label}. "
            f"Control point results: {pass_count} PASS, {minor_count} MINOR NC, "
            f"{major_count} MAJOR NC, {crit_count} CRITICAL NC."
        )

    @staticmethod
    def _build_markdown(
        inputs: GAP_FieldInputs,
        results: list[ControlPointResult],
        score: float,
        status: NCLevel,
        report_id: str,
        generated_at: str,
    ) -> str:
        STATUS_EMOJI = {
            NCLevel.PASS:        "✅ PASS",
            NCLevel.MINOR_NC:    "⚠️ MINOR NC",
            NCLevel.MAJOR_NC:    "🚨 MAJOR NC",
            NCLevel.CRITICAL_NC: "🛑 CRITICAL NC",
        }

        lines = [
            f"# GLOBALG.A.P. IFA v6 Compliance Report",
            f"",
            f"**Report ID:** `{report_id}`  ",
            f"**Generated:** {generated_at}  ",
            f"**Standard:** GLOBALG.A.P. IFA v6.0 — Fruits & Vegetables Module  ",
            f"",
            f"---",
            f"",
            f"## Farm & Field Details",
            f"| Field | {inputs.field_name} |",
            f"|---|---|",
            f"| Farm | {inputs.farm_name} |",
            f"| Grower ID | `{inputs.grower_id}` |",
            f"| Reporting Period | {inputs.report_period_start} → {inputs.report_period_end} |",
            f"",
            f"---",
            f"",
            f"## Certification Status",
            f"",
            f"**Overall Score: {score * 100:.1f} / 100**  ",
            f"**Status: {STATUS_EMOJI[status]}**",
            f"",
            f"---",
            f"",
            f"## Control Point Results",
            f"",
            f"| Control Point | Description | Score | Status |",
            f"|---|---|---|---|",
        ]

        for r in results:
            lines.append(f"| `{r.control_point_id}` | {r.description} | {r.score * 100:.0f}% | {STATUS_EMOJI[r.level]} |")

        lines += ["", "---", ""]

        for r in results:
            lines += [
                f"### `{r.control_point_id}` — {r.description}",
                f"",
                f"**Status:** {STATUS_EMOJI[r.level]}  **Score:** {r.score * 100:.0f}%",
                f"",
            ]
            if r.evidence:
                lines.append("**Evidence from FarmSense:**")
                for e in r.evidence:
                    lines.append(f"- {e}")
                lines.append("")
            if r.findings:
                lines.append("**Findings:**")
                for f_ in r.findings:
                    lines.append(f"- {f_}")
                lines.append("")
            if r.corrective_actions:
                lines.append("**Required Corrective Actions:**")
                for a in r.corrective_actions:
                    lines.append(f"1. {a}")
                lines.append("")

        lines += [
            "---",
            "",
            "*This report was generated automatically by FarmSense. Data provenance is "
            "verified via the FarmSense blockchain audit chain. This report does not "
            "constitute a formal GLOBALG.A.P. audit — a licensed certification body must "
            "conduct physical inspection for official certification.*",
        ]

        return "\n".join(lines)