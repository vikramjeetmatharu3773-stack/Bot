from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent.joinpath('.env'))

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
JWT_SECRET = os.getenv('JWT_SECRET', 'replace-me-in-prod')
JWT_ALGORITHM = 'HS256'
REFERRAL_REWARD = float(os.getenv('REFERRAL_REWARD', '0.5'))
WITHDRAWAL_MIN = float(os.getenv('WITHDRAWAL_MIN', '5.0'))
DATABASE_URL = os.getenv('DATABASE_URL', f"sqlite:///{BASE_DIR.parent.joinpath('data.db')}")
