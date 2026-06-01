import re
from typing import Optional, List
from sqlalchemy import select
from app.models.domain import Company

class NormalizationEngine:
    def __init__(self, db_session):
        self.db = db_session # Sync session for worker

    def clean_name(self, name: str) -> str:
        if not name: return ""
        name = name.upper().strip()
        name = re.sub(r'\b(LIMITED|LTD|PLC|CORP|CORPORATION|INC|ENTERPRISE|SERVICES)\b', '', name)
        name = re.sub(r'[^\w\s]', ' ', name)
        return " ".join(name.split())

    def find_canonical_identity(self, tin: str, name: str) -> Optional[Company]:
        if tin:
            company = self.db.execute(select(Company).where(Company.tin == tin)).scalars().first()
            if company: return company

        cleaned_name = self.clean_name(name)
        potential_matches = self.db.execute(select(Company).where(Company.name.ilike(f"%{cleaned_name}%"))).scalars().all()
        for match in potential_matches:
            if self.clean_name(match.name) == cleaned_name:
                return match
        return None

    def normalize_company(self, tin: str, name: str, address: str = "") -> Company:
        canonical = self.find_canonical_identity(tin, name)
        if canonical: return canonical

        new_company = Company(tin=tin, name=name, address=address, is_canonical=True)
        self.db.add(new_company)
        self.db.commit()
        self.db.refresh(new_company)
        return new_company
