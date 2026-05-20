from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Enum, Text, Boolean, Table
from sqlalchemy.orm import relationship
import enum
import datetime

Base = declarative_base()

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

    # Header Info
    declaration_date = Column(DateTime)
    office_code = Column(String, index=True)
    manifest_reg_number = Column(String)

    # Financials
    total_cif = Column(Float)
    total_fob = Column(Float)
    total_freight = Column(Float)
    currency_code = Column(String)
    exchange_rate = Column(Float)

    # Entities
    importer_id = Column(Integer, ForeignKey("companies.id"))
    exporter_id = Column(Integer, ForeignKey("companies.id"))
    declarant_id = Column(Integer, ForeignKey("companies.id"))
    bank_id = Column(Integer, ForeignKey("banks.id"))

    # Raw Data
    raw_json = Column(JSON)

    # Timestamps
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    importer = relationship("Company", foreign_keys=[importer_id])
    exporter = relationship("Company", foreign_keys=[exporter_id])
    declarant = relationship("Company", foreign_keys=[declarant_id])
    bank = relationship("Bank")
    items = relationship("GoodsItem", back_populates="declaration")
    containers = relationship("Container", back_populates="declaration")
    risk_findings = relationship("RiskFinding", back_populates="declaration")
    risk_scores = relationship("RiskScore", back_populates="declaration", uselist=False)

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    tin = Column(String, index=True) # Tax Identification Number
    rc_number = Column(String, index=True)
    name = Column(String, index=True)
    address = Column(Text)
    phone = Column(String)
    email = Column(String)

    # Normalization
    canonical_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    is_canonical = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class GoodsItem(Base):
    __tablename__ = "goods_items"

    id = Column(Integer, primary_key=True)
    declaration_id = Column(Integer, ForeignKey("declarations.id"))
    item_number = Column(Integer)
    hs_code = Column(String(10), index=True)
    commercial_description = Column(Text)

    # Quantities & Weights
    net_weight = Column(Float)
    gross_weight = Column(Float)
    quantity = Column(Float)
    unit_type = Column(String)

    # Values
    item_price = Column(Float)
    item_cif = Column(Float)

    # Relationships
    declaration = relationship("Declaration", back_populates="items")

class Container(Base):
    __tablename__ = "containers"

    id = Column(Integer, primary_key=True)
    declaration_id = Column(Integer, ForeignKey("declarations.id"))
    container_number = Column(String(20), index=True)
    container_size = Column(String(10))
    container_type = Column(String(20))
    seal_number = Column(String(50))

    declaration = relationship("Declaration", back_populates="containers")

class Bank(Base):
    __tablename__ = "banks"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)

class RiskScore(Base):
    __tablename__ = "risk_scores"

    id = Column(Integer, primary_key=True)
    declaration_id = Column(Integer, ForeignKey("declarations.id"))
    overall_score = Column(Float) # 0 to 100
    risk_level = Column(String) # Low, Medium, High, Critical

    # Breakdown
    valuation_score = Column(Float)
    hs_score = Column(Float)
    entity_score = Column(Float)
    anomaly_score = Column(Float)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    declaration = relationship("Declaration", back_populates="risk_scores")

class RiskFinding(Base):
    __tablename__ = "risk_findings"

    id = Column(Integer, primary_key=True)
    declaration_id = Column(Integer, ForeignKey("declarations.id"))
    category = Column(String) # Valuation, HS, Entity, etc.
    severity = Column(String) # Info, Warning, Error, Critical
    message = Column(Text)
    explanation = Column(Text)
    evidence = Column(JSON)
    score_impact = Column(Float)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    declaration = relationship("Declaration", back_populates="risk_findings")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    action = Column(String)
    resource_type = Column(String)
    resource_id = Column(String)
    payload = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class IntelligenceRemark(Base):
    __tablename__ = "intelligence_remarks"
    id = Column(Integer, primary_key=True)
    declaration_id = Column(Integer, ForeignKey("declarations.id"))
    user_id = Column(String)
    remark = Column(Text)
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
