from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    specifications = relationship("Specification", back_populates="user")


class Template(Base):
    __tablename__ = "templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String(50), nullable=False)
    complexity = Column(Integer, nullable=False)
    structure = Column(JSONB, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('type', 'complexity', name='uq_type_complexity'),
    )


class Specification(Base):
    __tablename__ = "specifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    template_id = Column(UUID(as_uuid=True), ForeignKey("templates.id"), nullable=True)
    title = Column(String(255), nullable=False)
    content = Column(JSONB, nullable=False, default=dict)
    type = Column(String(50), nullable=False)
    complexity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="specifications")
    template = relationship("Template")
    shared_link = relationship("SharedLink", back_populates="specification", uselist=False)


class SharedLink(Base):
    __tablename__ = "shared_links"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = Column(String(64), unique=True, nullable=False, index=True)
    spec_id = Column(UUID(as_uuid=True), ForeignKey("specifications.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    specification = relationship("Specification", back_populates="shared_link")
    
    __table_args__ = (
        UniqueConstraint('spec_id', name='uq_spec_shared_link'),
    )