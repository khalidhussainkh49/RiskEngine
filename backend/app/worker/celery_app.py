import httpx
import logging
import asyncio
from celery import Celery
from app.core.config import settings
from app.core.db import SessionLocal
from app.services.bodogwu_client import BodogwuClient
from app.services.normalization_engine import NormalizationEngine
from app.services.risk_engine import RiskEngine
from app.models.domain import Declaration, GoodsItem, DeclarationStatus

celery_app = Celery("ncdips_worker", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

def run_sync(coro):
    return asyncio.get_event_loop().run_until_complete(coro)

@celery_app.task
def process_declaration(sgd_id: str):
    db = SessionLocal()
    try:
        client = BodogwuClient()
        raw_data = run_sync(client.get_model(sgd_id))
        if not raw_data: return

        norm_engine = NormalizationEngine(db)
        importer = norm_engine.normalize_company(
            tin=raw_data.get('importerTin'),
            name=raw_data.get('importerName')
        )

        declaration = Declaration(
            sgd_id=sgd_id,
            importer_id=importer.id,
            total_cif=raw_data.get('totalCif'),
            status=DeclarationStatus.PROCESSED,
            raw_json=raw_data
        )
        db.add(declaration)
        db.flush()

        # Parse and save goods items
        for item_data in raw_data.get('items', []):
            item = GoodsItem(
                declaration_id=declaration.id,
                item_number=item_data.get('itemNumber'),
                hs_code=item_data.get('hsCode'),
                commercial_description=item_data.get('description'),
                item_price=item_data.get('price'),
                quantity=item_data.get('quantity'),
                unit_type=item_data.get('unit')
            )
            db.add(item)

        db.flush()

        # Risk Scoring
        risk_engine = RiskEngine(declaration)
        # Note: valuation/HS engines need to be refactored to sync or run_sync correctly
        score = risk_engine.calculate_overall_score()
        db.add(score)

        for finding in risk_engine.findings:
            db.add(finding)

        declaration.status = DeclarationStatus.RISK_ASSESSED
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
