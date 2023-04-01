from sqlalchemy.orm import Session

from . import models, schemas

import geopy.distance

def get_contact_by_name(db: Session, name: str):
    return db.query(models.Contact).filter(models.Contact.name == name).first()


def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Contact).offset(skip).limit(limit).all()


def create_contact(db: Session, contact: schemas.ContactCreate):
    contact = models.Contact(name=contact.name, mobile_number=contact.mobile_number)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

def delete_contact(db: Session, contact_id: int):
    db.query(models.Contact).filter(models.Contact.id == contact_id).delete()
    db.commit()
    return {"Message": "Record Deleted!"}

def update_contact(db: Session, contact_id: int, new_name:str, new_mobile: int):
    contact_to_be_updated = db.query(models.Contact).filter(models.Contact.id == contact_id)
    contact_to_be_updated.name = new_name
    contact_to_be_updated.mobile_number = new_mobile
    db.commit()
    return {"Message": "Record Updated!"}

def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Coordinates).offset(skip).limit(limit).all()


def create_contact_address(db: Session, coordinates: schemas.CoordinatesCreate, contact_id: int):
    db_coordinates = models.Coordinates(**coordinates.dict(), contact_id=contact_id)
    db.add(db_coordinates)
    db.commit()
    db.refresh(db_coordinates)
    return db_coordinates

def get_addresses_by_distance(db: Session, name: str, distance: int):
    list_of_addresses = get_addresses(db)
    address_of_source = db.query(models.Contact).filter(models.Contact.name == name).first().address[0]
    source_address_contact_id = address_of_source.contact_id
    source_coordinates = (float(address_of_source.latitude),float(address_of_source.longitude))
    contact_id_list = []
    for address in list_of_addresses:
        target_coordinates = (float(address.latitude),float(address.longitude))
        if geopy.distance.distance(source_coordinates,target_coordinates).km < distance and address.contact_id != source_address_contact_id:
            contact_id_list.append(address.contact_id)
    
    final_result = db.query(models.Contact).filter(models.Contact.id.in_(contact_id_list)).all()
    return final_result
