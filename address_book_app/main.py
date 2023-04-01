from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import address_book_actions, models, schemas
from .db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = address_book_actions.get_contact_by_name(db, name=contact.name)
    if db_contact:
        raise HTTPException(status_code=400, detail="Name already registered")
    return address_book_actions.create_contact(db=db, contact=contact)


@app.get("/contacts/", response_model=List[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = address_book_actions.get_contacts(db, skip=skip, limit=limit)
    return contacts


@app.post("/contacts/{contact_id}/address/", response_model=schemas.Coordinates)
def create_address_for_contact(
    contact_id: int, coordinates: schemas.CoordinatesCreate, db: Session = Depends(get_db)
):
    return address_book_actions.create_contact_address(db=db, coordinates=coordinates, contact_id=contact_id)


@app.get("/address/", response_model=List[schemas.Coordinates])
def read_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    addresses = address_book_actions.get_addresses(db, skip=skip, limit=limit)
    return addresses


@app.get("/contactsbydistance/")
def get_contacts_by_distance(name:str, distance:int, db: Session = Depends(get_db)):
    addresses = address_book_actions.get_addresses_by_distance(db,name,distance)
    return addresses


@app.delete("/contact")
def delete_contact_by_id(contact_id:int, db: Session = Depends(get_db)):
    return address_book_actions.delete_contact(db,contact_id)

@app.put("/contact")
def update_contact_by_id(contact_id:int, new_name:str, new_mobile:int, db: Session = Depends(get_db)):
    return address_book_actions.update_contact(db,contact_id,new_name,new_mobile)