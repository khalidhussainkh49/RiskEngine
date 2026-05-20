from sentence_transformers import SentenceTransformer, util
import torch

class HSValidationEngine:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def calculate_semantic_similarity(self, declaration_description: str, hs_description: str) -> float:
        """Calculate semantic similarity between commercial description and official HS description."""
        embeddings = self.model.encode([declaration_description, hs_description], convert_to_tensor=True)
        similarity = util.cos_sim(embeddings[0], embeddings[1])
        return float(similarity[0][0])

    def validate_hs_match(self, declaration_description: str, hs_description: str, threshold: float = 0.4):
        """Validate if the commercial description matches the HS code's official description."""
        similarity = self.calculate_semantic_similarity(declaration_description, hs_description)

        is_suspicious = similarity < threshold

        return {
            "similarity": similarity,
            "is_suspicious": is_suspicious,
            "confidence": 0.85 if is_suspicious else 0.9
        }
