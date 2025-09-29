from fastapi import FastAPI
from .router import user,book,auth
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
app=FastAPI()

models.Base.metadata.create_all(bind=engine)

origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(book.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return "Hello World1"