from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
import jwt
from .config import JWT_SECRET, JWT_ALGORITHM, ADMIN_PASSWORD
from .database import SessionLocal
from .models import User, WithdrawalRequest, GamePartner

templates = Jinja2Templates(directory="../templates")
router = APIRouter(prefix="/admin")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_admin(password: str):
    return password == ADMIN_PASSWORD


@router.get('/login')
def login_page(request: Request):
    return templates.TemplateResponse('admin_login.html', {"request": request})


@router.post('/login')
def do_login(password: str = Form(...)):
    if not verify_admin(password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid')
    token = jwt.encode({"role": "admin"}, JWT_SECRET, algorithm=JWT_ALGORITHM)
    resp = RedirectResponse(url='/admin/dashboard', status_code=302)
    resp.set_cookie('token', token, httponly=True)
    return resp


@router.get('/dashboard')
def dashboard(request: Request):
    session = SessionLocal()
    users = session.query(User).count()
    withdrawals = session.query(WithdrawalRequest).filter_by(approved=False).count()
    games = session.query(GamePartner).all()
    session.close()
    return templates.TemplateResponse('admin_dashboard.html', {"request": request, "users": users, "withdrawals": withdrawals, "games": games})
