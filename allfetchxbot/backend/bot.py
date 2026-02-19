from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from .config import TELEGRAM_BOT_TOKEN
from .database import SessionLocal
from .models import User
from fastapi import url_for

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    ref = args[0] if args else None
    telegram_id = str(update.effective_user.id)
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            user = User(telegram_id=telegram_id, username=update.effective_user.username)
            if ref:
                ref_user = session.query(User).filter_by(telegram_id=ref).first()
                if ref_user:
                    user.referrer_id = ref_user.id
            session.add(user)
            session.commit()
        keyboard = [[InlineKeyboardButton('Open AllFetchX', web_app=None)]]
        # web_app will be handled by Telegram WebApp on client side; placeholder here
        await update.message.reply_text('Welcome to AllFetchX! Use the mini app to get started.', reply_markup=InlineKeyboardMarkup(keyboard))
    finally:
        session.close()


def run_bot():
    if not TELEGRAM_BOT_TOKEN:
        print('No TELEGRAM_BOT_TOKEN set; bot will not start')
        return
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    print('Starting bot...')
    app.run_polling()

if __name__ == '__main__':
    run_bot()
