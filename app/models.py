from app.database import Base
from sqlalchemy import Integer,String,Column,Boolean,TIMESTAMP,text,func,ForeignKey
from sqlalchemy.orm import relationship

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    added_by_user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    added_by_user = relationship("User")

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,index=True,nullable=False,unique=True)
    password=Column(String,index=True,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text('now()'),nullable=False)

    
