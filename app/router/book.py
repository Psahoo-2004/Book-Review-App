from fastapi import APIRouter,Depends,HTTPException
from .. import schemas,models,oauth2
from sqlalchemy.orm import session
from ..database import get_db
from .. models import Book


router=APIRouter(
    prefix="/book",
    tags=["Book"]
)

@router.post("/",response_model=schemas.RecordOut)
def create_record(book:schemas.CreateRecord,db:session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    CR=Book(added_by_user_id=current_user.id,**book.model_dump())
    db.add(CR)
    db.commit()
    db.refresh(CR)
    return CR

@router.get("/",response_model=list[schemas.RecordOut])
def get_record(db:session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    GR=db.query(Book).all()
    return GR

@router.get("/{id}",response_model=list[schemas.RecordOut])
def get_record(id:int,db:session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    CRI=db.query(Book).filter(Book.added_by_user_id == current_user.id and Book.id == id).all()
    if not CRI:
        raise HTTPException(status_code=404,detail="Record not found")
    return CRI

@router.put("/{id}",response_model=schemas.RecordOut)
def UpdateRecord(id:int,book:schemas.UpdateRecord,db:session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    UB=db.query(Book).filter(Book.id==id).first()
    if not UB:
        raise HTTPException(status_code=404,detail="Record not found")
    if UB.added_by_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    for key,value in book.model_dump().items():
        setattr(UB,key,value)
    db.commit()
    db.refresh(UB)
    return UB


@router.delete("/{id}", response_model=schemas.RecordOut)
def delete_record(id: int,db: session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    DB = db.query(Book).filter(Book.id == id).first()
    if not DB:
        raise HTTPException(status_code=404, detail="Record not found")
    if DB.added_by_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(DB)
    db.commit()
    return DB


