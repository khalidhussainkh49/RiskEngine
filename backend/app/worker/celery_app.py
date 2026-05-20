from celery import Celery
from app.core.config import settings
from app.services.bodogwu_client import BodogwuClient
from app.services.normalization_engine import NormalizationEngine
from app.services.risk_engine import RiskEngine
from app.services.valuation_intelligence import ValuationIntelligence
from app.services.hs_validation_engine import HSValidationEngine
from app.models.domain import Declaration, DeclarationStatus
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
import asyncio

celery_app = Celery("ncdips_worker", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

@celery_app.task
def poll_bodogwu():
    client = BodogwuClient()
    loop = asyncio.get_event_loop()
    models = loop.run_until_complete(client.get_models())
    for model in models:
        process_declaration.delay(model['sgdId'])

@celery_app.task
def process_declaration(sgd_id: str):
    db = SessionLocal()
    try:
        client = BodogwuClient()
        loop = asyncio.get_event_loop()
        raw_data = loop.run_until_complete(client.get_model(sgd_id))

        if not raw_data:
            return

        # 1. Normalize Entities
        norm_engine = NormalizationEngine(db)
        importer = loop.run_until_complete(norm_engine.normalize_company(
            tin=raw_data.get('importerTin'),
            name=raw_data.get('importerName')
        ))

        # 2. Save Declaration
        declaration = Declaration(
            sgd_id=sgd_id,
            importer_id=importer.id,
            total_cif=raw_data.get('totalCif'),
            status=DeclarationStatus.PROCESSED,
            raw_json=raw_data
        )
        db.add(declaration)
        db.flush()

        # 3. Risk Scoring
        risk_engine = RiskEngine(declaration)

        # Valuation Check
        valuation_intel = ValuationIntelligence(db)
        for item in declaration.items:
            anomaly = loop.run_until_complete(valuation_intel.detect_valuation_anomaly(
                item.hs_code, item.item_price, item.unit_type
            ))
            if anomaly:
                risk_engine.add_finding(
                    category="Valuation",
                    severity="High" if anomaly['type'] == "undervaluation" else "Warning",
                    message=f"Suspicious {anomaly['type']}",
                    explanation=f"Z-Score: {anomaly['z_score']}",
                    impact=25.0 if anomaly['type'] == "undervaluation" else 10.0
                )

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
