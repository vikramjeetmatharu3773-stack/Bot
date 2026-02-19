from .database import SessionLocal
from .models import User, Transaction, WithdrawalRequest

def get_balance(telegram_id):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            return 0.0
        return dict(balance=user.balance, pending=user.pending)
    finally:
        session.close()

def request_withdrawal(telegram_id, amount, address):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user or user.balance < amount:
            return None
        wr = WithdrawalRequest(user_id=user.id, amount=amount, address=address)
        user.balance -= amount
        session.add(wr)
        session.commit()
        return wr
    finally:
        session.close()
