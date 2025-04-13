from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import EmailStr
import bcrypt
from database import SessionLocal, engine
from models import User
from schemas import UserCreate, UserLogin, UserResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to hash the password
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return password_hash.decode('utf-8')

# Function to verify the password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), password_hash.encode('utf-8'))

@app.post("/signup", response_model=UserResponse)
async def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    if user.password != user.password_confirmation:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password before saving to the database
    password_hash = hash_password(user.password)

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        gender=user.gender,
        phone=user.phone,
        password=password_hash
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": "Login successful", "user": {"id": db_user.id, "email": db_user.email}}

