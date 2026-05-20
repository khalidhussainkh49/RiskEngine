import re
from typing import Optional, List
from sqlalchemy.future import select
from app.models.domain import Company

class NormalizationEngine:
    def __init__(self, db_session):
        self.db = db_session

    def clean_name(self, name: str) -> str:
        """Clean and normalize company names."""
        if not name:
            return ""
        name = name.upper().strip()
        # Remove common suffixes and punctuation
        name = re.sub(r'\b(LIMITED|LTD|PLC|CORP|CORPORATION|INC|ENTERPRISE|SERVICES)\b', '', name)
        name = re.sub(r'[^\w\s]', ' ', name)
        name = " ".join(name.split())
        return name

    async def find_canonical_identity(self, tin: str, name: str) -> Optional[Company]:
        """Find or create a canonical identity for a company."""
        # 1. Exact match by TIN
        if tin:
            result = await self.db.execute(select(Company).where(Company.tin == tin))
            company = result.scalars().first()
            if company:
                return company

        # 2. Match by cleaned name (simplified fuzzy)
        cleaned_name = self.clean_name(name)
        result = await self.db.execute(select(Company).where(Company.name.ilike(f"%{cleaned_name}%")))
        potential_matches = result.scalars().all()

        for match in potential_matches:
            if self.clean_name(match.name) == cleaned_name:
                return match

        return None

    async def normalize_company(self, tin: str, name: str, address: str = "") -> Company:
        """Resolve or create a company entity."""
        canonical = await self.find_canonical_identity(tin, name)
        if canonical:
            return canonical

        new_company = Company(
            tin=tin,
            name=name,
            address=address,
            is_canonical=True
        )
        self.db.add(new_company)
        await self.db.commit()
        await self.db.refresh(new_company)
        return new_company
