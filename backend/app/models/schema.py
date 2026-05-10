from sqlalchemy import Column, Integer, String, Date, Text, Boolean, TIMESTAMP, JSON 
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.core.database import Base
from datetime import datetime

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True)
    arxiv_id = Column(String, unique=True, nullable=False)
    title = Column(String)
    authors = Column(String)
    abstract = Column(Text)
    categories = Column(JSON)
    pdf_url = Column(String)
    published_at = Column(Date)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_vectorized = Column(Boolean, default=False)

class Brief(Base):
    __tablename__ = "briefings"

    id = Column(Integer, primary_key=True)
    paper_id = Column(Integer, ForeignKey('papers.id'), nullable=False)
    title = Column(String)
    summary_en = Column(Text)
    summary_ko = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    discord_sent = Column(Boolean, default=False)

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    session_id = Column(String, nullable=False)
    role = Column(String)
    content = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)
    categories = Column(JSON)
    keywords = Column(JSON)
    max_results = Column(Integer, default=5)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)