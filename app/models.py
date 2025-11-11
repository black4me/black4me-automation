from sqlalchemy import Column, String, Float, DateTime, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel

Base = declarative_base()
engine = create_engine("sqlite:///leads.db", echo=False)

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    fw_order_id = Column(String, unique=True, index=True)
    email = Column(String, index=True)
    name = Column(String)
    product = Column(String)
    amount = Column(Float)
    tags = Column(String, default="")  # comma separated
    created = Column(DateTime, server_default=func.now())
    status = Column(String, default="new")  # new / upsell_sent / vip / bought_upsell / member

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, index=True)
    channel = Column(String)  # email / whatsapp
    subject = Column(String)
    body = Column(String)
    scheduled_at = Column(DateTime)
    sent_at = Column(DateTime, nullable=True)
    opened = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)
