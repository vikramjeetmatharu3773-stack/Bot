# AllFetchXBot

AllFetchXBot is a Telegram Bot + Telegram Mini App platform for transparent earning and search.

Quick start

1. Copy `.env.example` to `.env` and set `TELEGRAM_BOT_TOKEN` and `ADMIN_PASSWORD`.
2. Create a Python 3.11+ venv and install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run the FastAPI backend:

```bash
uvicorn allfetchxbot.backend.main:app --reload --port 8000
```

4. (Optional) Run the bot process:

```bash
python -m allfetchxbot.backend.bot
```

Notes
- Only public resources are searched. Adjust `SAFE_DOMAINS` in `search_engine.py`.
- Transparent referral reward is configured via environment `REFERRAL_REWARD`.
- This scaffold is production-ready in structure; replace defaults and secrets before deploying.

Telegram Mini App integration
- Use the Web App URL pointing to `https://yourhost/miniapp` in BotFather or inline keyboard web_app.
# Bot