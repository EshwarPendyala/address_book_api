from typing import List, Union

from pydantic import BaseModel


class CoordinatesBase(BaseModel):
    longitude: float
    latitude: float


class CoordinatesCreate(CoordinatesBase):
    pass


class Coordinates(CoordinatesBase):
    id: int
    contact_id: int

    class Config:
        orm_mode = True


class ContactBase(BaseModel):
    name: str
    mobile_number: int


class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    address: List[Coordinates] = []

    class Config:
        orm_mode = True