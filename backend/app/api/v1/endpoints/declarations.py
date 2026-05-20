from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from app.core.db import get_db
from app.models.domain import Declaration

router = APIRouter()

@router.get("/")
async def get_declarations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Declaration)
        .options(selectinload(Declaration.risk_scores), selectinload(Declaration.importer))
        .order_by(Declaration.created_at.desc())
        .limit(100)
    )
    return result.scalars().all()

@router.get("/{sgd_id}")
async def get_declaration(sgd_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Declaration)
        .where(Declaration.sgd_id == sgd_id)
        .options(
            selectinload(Declaration.items),
            selectinload(Declaration.risk_findings),
            selectinload(Declaration.risk_scores),
            selectinload(Declaration.importer),
            selectinload(Declaration.exporter)
        )
    )
    declaration = result.scalar_one_or_none()
    if not declaration:
        raise HTTPException(status_code=404, detail="Declaration not found")
    return declaration
