from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UpdateUser(BaseModel):
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class RecordBase(BaseModel):
    title: str
    author: str

    class Config:
        from_attributes = True

class CreateRecord(RecordBase):
    pass

class UpdateRecord(RecordBase):
    title: str
    author: str

    class Config:
        from_attributes = True

class Record(BaseModel):
    id: int
    added_by_user: UserOut  # Changed here to reflect nested User object

    class Config:
        from_attributes = True

class RecordOut(BaseModel):
    id: int
    title: str
    author: str
    added_by_user: UserOut  # Changed here too

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None