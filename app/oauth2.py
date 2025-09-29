from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas,models,database
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer,HTTPBearer
from sqlalchemy.orm import Session
from .config import settings

bearer_scheme=HTTPBearer()
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY=settings.SECRET_KEY
ALGORITHM=settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_TIME=settings.ACCESS_TOKEN_EXPIRE_TIME

def create_access_token(data:dict):
    to_encode=data
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=401,detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    token=verify_access_token(token,credentials_exception)
    user = db.get(models.User, token.id)
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User does not exists")
    return user
