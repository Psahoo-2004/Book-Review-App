from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from .. import database,schemas,models,oauth2
from .. database import get_db
from .. utils import hashed, verify_password

router=APIRouter(prefix="/user",
                 tags=["User"])

@router.post("/",response_model=schemas.UserOut)
def create_user(users:schemas.UserCreate,db:Session=Depends(get_db)):
    check_user=db.query(models.User).filter(models.User.email == users.email).first()
    if check_user:
        raise HTTPException(status_code=400,detail="User already exists")
    hashed_password=hashed(users.password)
    users.password=hashed_password

    CU=models.User(**users.model_dump())
    db.add(CU)
    db.commit()
    db.refresh(CU)
    return CU


@router.get("/",response_model=list[schemas.UserOut])
def get_user(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    users=db.query(models.User).all()
    return users

@router.get("/{id}",response_model=schemas.UserOut)
def get_user_by_id(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    GU=db.query(models.User).filter(models.User.id==current_user.id).first()
    if GU:
        return GU
    raise HTTPException(status_code=404,detail="User doesnot exists")

@router.put("/{id}", response_model=schemas.UserOut)
def update_user(users: schemas.UpdateUser,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    UU = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not UU:
        raise HTTPException(status_code=404, detail="User does not exist")

    update_data = users.model_dump(exclude_unset=True)

    # Handle password separately
    if "password" in update_data:
        if verify_password(update_data["password"], UU.password):
            raise HTTPException(status_code=400, detail="Please use a different password")
        # Hash password
        update_data["password"] = hashed(update_data["password"])

    # Update only the fields present in update_data
    for key, value in update_data.items():
        setattr(UU, key, value)

    db.commit()
    db.refresh(UU)
    return UU


@router.delete("/{id}",response_model=schemas.UserOut)
def delete_user(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    DU=db.query(models.User).filter(models.User.id == current_user.id).first()
    if not DU:
        raise HTTPException(status_code=404,detail="User doesnot exists")
    db.delete(DU)
    db.commit()
    return DU
