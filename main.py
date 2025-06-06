from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import SessionLocal,engine
import models

models.Base.metadata.create_all(bind=engine)
app= FastAPI()

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ContactCreate(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    message: str

@app.post("/contact")
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact=models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return {"message":"お問い合わせを受け付けました"}

@app.get("/contacts")
def read_contacts(db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).all()
    return contacts