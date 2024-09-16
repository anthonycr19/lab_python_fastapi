from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

from passlib.context import CryptContext

from jose import JWTError, jwt
from typing import Optional, List
from datetime import datetime, timedelta

from ..model.model import User

#SQLACHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost:5433/inka_company'
SQLACHEMY_DATABASE_URL = settings.db_url
engine = create_engine(SQLACHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Configurar Password Hashin
pwd_context = CryptContext(schemes=["bcrypt"])

# Configuración JWT
SECRET_KEY = "secreakay2460*"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuración de OAUTH2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first

#Function to get user by username
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


#Authenticate user
def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    print("Usuariooo {}".format(user.__dict__))
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


# Dependencia para obtener el usuario actual a partir del token
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
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

    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


