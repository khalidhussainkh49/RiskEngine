from typing import List, Dict, Any
from app.models.domain import Declaration, RiskFinding, RiskScore

class RiskEngine:
    def __init__(self, declaration: Declaration):
        self.declaration = declaration
        self.findings = []
        self.total_impact = 0

    def add_finding(self, category: str, severity: str, message: str, explanation: str, impact: float, evidence: Dict[str, Any] = None):
        finding = RiskFinding(
            declaration_id=self.declaration.id,
            category=category,
            severity=severity,
            message=message,
            explanation=explanation,
            score_impact=impact,
            evidence=evidence
        )
        self.findings.append(finding)
        self.total_impact += impact

    def analyze_valuation_risk(self):
        """Check for valuation anomalies."""
        # This will be refined with the Valuation Intelligence Engine
        pass

    def analyze_hs_code_risk(self):
        """Check for HS code mismatches."""
        # This will be refined with the HS Validation Engine
        pass

    def analyze_entity_risk(self):
        """Check for suspicious entities."""
        # Example rule: New importer with high-value declaration
        if self.declaration.total_cif > 1000000 and self.declaration.importer.created_at.date() == self.declaration.created_at.date():
             self.add_finding(
                 category="Entity",
                 severity="Warning",
                 message="High-value declaration from new importer",
                 explanation="The importer was first seen today and is declaring goods worth over $1M.",
                 impact=15.0
             )

    def analyze_operational_risk(self):
        """Check for operational anomalies (weights, quantities)."""
        for item in self.declaration.items:
            if item.gross_weight == 0:
                self.add_finding(
                    category="Operational",
                    severity="Error",
                    message=f"Zero gross weight for item {item.item_number}",
                    explanation="Item gross weight cannot be zero.",
                    impact=20.0
                )

    def calculate_overall_score(self) -> RiskScore:
        self.analyze_entity_risk()
        self.analyze_operational_risk()
        self.analyze_valuation_risk()
        self.analyze_hs_code_risk()

        # Clamp score between 0 and 100
        overall_score = min(max(self.total_impact, 0), 100)

        risk_level = "Low"
        if overall_score > 75: risk_level = "Critical"
        elif overall_score > 50: risk_level = "High"
        elif overall_score > 25: risk_level = "Medium"

        return RiskScore(
            declaration_id=self.declaration.id,
            overall_score=overall_score,
            risk_level=risk_level,
            valuation_score=0.0, # To be updated
            hs_score=0.0,
            entity_score=0.0,
            anomaly_score=0.0
        )
