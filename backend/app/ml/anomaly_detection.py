from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np
from typing import List, Dict, Any

class AnomalyDetectionML:
    def __init__(self):
        self.model = IsolationForest(contamination=0.05, random_state=42)

    def train_on_declarations(self, data: pd.DataFrame):
        """Train Isolation Forest on historical declaration features."""
        # Features: CIF, Freight Ratio, Weight per Unit, etc.
        features = ['total_cif', 'freight_ratio', 'weight_per_unit']
        self.model.fit(data[features])

    def predict_anomaly(self, features: Dict[str, float]) -> bool:
        """Predict if a new declaration is an anomaly."""
        df = pd.DataFrame([features])
        prediction = self.model.predict(df)
        return prediction[0] == -1

class ExplainableAI:
    @staticmethod
    def generate_explanation(finding_type: str, evidence: Dict[str, Any]) -> str:
        """Generate human-readable explanations for risk findings."""
        if finding_type == "undervaluation":
            return (f"The declared unit price is significantly lower than the historical average "
                    f"for this HS code. Historical average: {evidence.get('avg'):.2f}, "
                    f"Z-Score: {evidence.get('z_score'):.2f}.")

        if finding_type == "hs_mismatch":
            return (f"The commercial description does not semantically align with the official "
                    f"HS code description. Similarity score: {evidence.get('similarity'):.2%}.")

        return "Anomaly detected based on historical behavioral patterns."
