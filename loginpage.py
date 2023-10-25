from fastapi import FastAPI, Depends, HTTPException, status, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from fastapi import Cookie


app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./login.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Template setup
templates = Jinja2Templates(directory="templates")

# Security setup
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User model
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)

class TokenData(BaseModel):
    username: str

# Function to authenticate user
def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if user and pwd_context.verify(password, user.password):
        return user
    return None

# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to get current user from token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Login route with token-based authentication
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Your login route with token-based authentication
@app.post("/login/", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(username, password, db)
    if user:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
        return templates.TemplateResponse("home.html", {"request": request, "message": "Login successful", "username": username, "access_token": access_token}).body
    else:
        error_message = "Incorrect username or password. Please try again."
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user is None:
            error_message = "Username not recognized. Please register to create an account."
        return templates.TemplateResponse("login.html", {"request": request, "message": error_message}).body

@app.post("/signup/",response_class=HTMLResponse)
async def signup(request: Request,username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == username).first()

    if existing_user:
        # User already exists, return a message
        return templates.TemplateResponse("signup.html", {"request": request, "message": "User already exists. Please log in."})
    else:
        # Hash the password and create a new user
        hashed_password = pwd_context.hash(password)
        user = User(username=username, password=hashed_password)
        db.add(user)
        db.commit()
        return templates.TemplateResponse("login.html", {"request": request})
    
@app.get("/", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": ""})

@app.get("/signup/",response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html",{"request":request})

@app.get("/login/",response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("login.html",{"request":request})


session_data = {}

@app.post("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    # Clear session data
    session_id = request.cookies.get("session_id")
    if session_id in session_data:
        del session_data[session_id]

    # Redirect the user to the login page
    response = templates.TemplateResponse("login.html", {"request": request})
    response.delete_cookie(key="session_id")  # Clear session ID cookie
    return response