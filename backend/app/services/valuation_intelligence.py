import numpy as np
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.domain import GoodsItem

class ValuationIntelligence:
    def __init__(self, db_session):
        self.db = db_session

    async def get_historical_stats(self, hs_code: str, unit_type: str):
        """Calculate historical unit price stats for an HS code."""
        query = (
            select(
                func.avg(GoodsItem.item_price / GoodsItem.quantity).label('avg_price'),
                func.stddev(GoodsItem.item_price / GoodsItem.quantity).label('std_price'),
                func.count(GoodsItem.id).label('count')
            )
            .where(GoodsItem.hs_code == hs_code)
            .where(GoodsItem.unit_type == unit_type)
            .where(GoodsItem.quantity > 0)
        )
        result = await self.db.execute(query)
        return result.one_or_none()

    async def detect_valuation_anomaly(self, hs_code: str, unit_price: float, unit_type: str):
        """Detect if a unit price is a statistical outlier."""
        stats = await self.get_historical_stats(hs_code, unit_type)
        if not stats or stats.count < 10:
            return None # Not enough data for statistical analysis

        avg = stats.avg_price
        std = stats.std_price

        if std == 0: return None

        z_score = (unit_price - avg) / std

        if z_score < -2:
            return {
                "type": "undervaluation",
                "z_score": z_score,
                "avg": avg,
                "confidence": 0.8
            }
        elif z_score > 3:
            return {
                "type": "overvaluation",
                "z_score": z_score,
                "avg": avg,
                "confidence": 0.7
            }

        return None
