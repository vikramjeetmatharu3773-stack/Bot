from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    balance = Column(Float, default=0.0)
    pending = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    referrer_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    referrals = relationship('User', backref='referrer', remote_side=[id])


class Referral(Base):
    __tablename__ = 'referrals'
    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey('users.id'))
    referred_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    kind = Column(String)  # e.g., 'referral','game','withdrawal'
    created_at = Column(DateTime, default=datetime.utcnow)
    meta = Column(Text, nullable=True)


class GamePartner(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)
    commission = Column(Float, default=0.1)
    clicks = Column(Integer, default=0)
    active = Column(Boolean, default=True)


class WithdrawalRequest(Base):
    __tablename__ = 'withdrawals'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    address = Column(String)
    approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
