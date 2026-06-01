from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum
import datetime

class DeclarationStatus(enum.Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    RISK_ASSESSED = "risk_assessed"
    FAILED = "failed"

class Declaration(Base):
    __tablename__ = "declarations"

    id = Column(Integer, primary_key=True)
    sgd_id = Column(String, unique=True, index=True)
    status = Column(Enum(DeclarationStatus), default=DeclarationStatus.PENDING)
    declaration_date = Column(DateTime)
    total_cif = Column(Float)
    importer_id = Column(Integer, ForeignKey("companies.id"))
    raw_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    importer = relationship("Company", foreign_keys=[importer_id])
    items = relationship("GoodsItem", back_populates="declaration")
    risk_findings = relationship("RiskFinding", back_populates="declaration")
    risk_scores = relationship("RiskScore", back_populates="declaration", uselist=False)

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    tin = Column(String, index=True)
    name = Column(String, index=True)
    address = Column(Text)
    is_canonical = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class GoodsItem(Base):
    __tablename__ = "goods_items"
    id = Column(Integer, primary_key=True)
    declaration_id = Column(Integer, ForeignKey("declarations.id"))
    hs_code = Column(String(10), index=True)
    item_price = Column(Float)
    quantity = Column(Float)
    unit_type = Column(String)
    declaration = relationship("Declaration", back_populates="items")

class RiskScore(Base):
    __tablename__ = "risk_scores"
    id = Column(Integer, primary_key=True)
    declaration_id = Column(Integer, ForeignKey("declarations.id"))
    overall_score = Column(Float)
    declaration = relationship("Declaration", back_populates="risk_scores")

class RiskFinding(Base):
    __tablename__ = "risk_findings"
    id = Column(Integer, primary_key=True)
    declaration_id = Column(Integer, ForeignKey("declarations.id"))
    category = Column(String)
    message = Column(Text)
    score_impact = Column(Float)
    declaration = relationship("Declaration", back_populates="risk_findings")
