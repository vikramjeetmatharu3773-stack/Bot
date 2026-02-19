from fastapi import FastAPI, Request, Depends, HTTPException, status, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from .database import init_db, SessionLocal
from .models import User
from .config import TELEGRAM_BOT_TOKEN, WITHDRAWAL_MIN
import jwt
from .admin import router as admin_router
from .search_engine import search_query

app = FastAPI(title='AllFetchXBot')
app.mount('/static', StaticFiles(directory='../static'), name='static')
templates = Jinja2Templates(directory='../templates')


@app.on_event('startup')
async def startup_event():
    init_db()


@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@app.get('/miniapp', response_class=HTMLResponse)
def miniapp(request: Request):
    return templates.TemplateResponse('dashboard.html', {"request": request})


@app.post('/api/search')
async def api_search(q: str = Form(...)):
    results = await search_query(q)
    return JSONResponse({'results': results})


@app.post('/api/register')
def api_register(telegram_id: str = Form(...), username: str | None = None):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            user = User(telegram_id=telegram_id, username=username)
            session.add(user)
            session.commit()
        return {'ok': True}
    finally:
        session.close()


app.include_router(admin_router)
