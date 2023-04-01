from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, index=True)
    mobile_number = Column(Integer)
    address  = relationship("Coordinates", back_populates="contact")


class Coordinates(Base):
    __tablename__ = "coordinates"

    id = Column(Integer, primary_key=True, index=True)
    longitude = Column(Float, index=True)
    latitude = Column(Float, index=True)
    contact_id = Column(Integer, ForeignKey("contact.id"))
    contact = relationship("Contact", back_populates="address")