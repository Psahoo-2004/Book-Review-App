from fastapi import APIRouter,HTTPException,Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database,models,schemas,utils,oauth2

router=APIRouter(
    prefix="/login",
    tags=['Authentication']
)

@router.post("/")
def user_login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    UL=db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not UL:
        raise HTTPException(status_code=401,detail="Invalid Credentials")
    verify1=utils.verify_password(user_credentials.password,UL.password)
    if not verify1:
        raise HTTPException(status_code=401,detail="Invalid Credentials")
    
    access_token=oauth2.create_access_token(data={"user_id":UL.id})
    return {"access_token":access_token,"token_type":"bearer"}