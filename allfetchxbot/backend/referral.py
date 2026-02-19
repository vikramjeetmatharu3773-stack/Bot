from .database import SessionLocal
from .models import User, Referral
from .config import REFERRAL_REWARD

def create_referral(referrer_telegram_id, referred_telegram_id, session: SessionLocal = None):
    close = False
    if session is None:
        session = SessionLocal()
        close = True
    try:
        referrer = session.query(User).filter_by(telegram_id=referrer_telegram_id).first()
        referred = session.query(User).filter_by(telegram_id=referred_telegram_id).first()
        if not referrer or not referred:
            return False
        # record referral
        r = Referral(referrer_id=referrer.id, referred_id=referred.id)
        session.add(r)
        # give transparent reward to referrer
        referrer.balance += REFERRAL_REWARD
        session.commit()
        return True
    finally:
        if close:
            session.close()
