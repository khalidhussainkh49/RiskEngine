from typing import List, Dict, Any
from app.models.domain import Declaration, RiskFinding, RiskScore

class RiskEngine:
    def __init__(self, declaration: Declaration, valuation_intel=None, hs_engine=None):
        self.declaration = declaration
        self.findings = []
        self.total_impact = 0
        self.valuation_intel = valuation_intel
        self.hs_engine = hs_engine

    def add_finding(self, category: str, message: str, impact: float):
        finding = RiskFinding(
            declaration_id=self.declaration.id,
            category=category,
            message=message,
            score_impact=impact
        )
        self.findings.append(finding)
        self.total_impact += impact

    def analyze_valuation(self):
        if not self.valuation_intel: return
        for item in self.declaration.items:
            anomaly = self.valuation_intel.detect_valuation_anomaly(
                item.hs_code, item.item_price, item.unit_type
            )
            if anomaly:
                self.add_finding("Valuation", f"Suspicious {anomaly['type']}", 25.0)

    def calculate_overall_score(self) -> RiskScore:
        self.analyze_valuation()
        overall_score = min(max(self.total_impact, 0), 100)
        return RiskScore(
            declaration_id=self.declaration.id,
            overall_score=overall_score
        )
