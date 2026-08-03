from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.database import Base

class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique = True, index = True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False, default="customer")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key = True, index= True)
    name = Column(String, nullable = False)
    event_date = Column (DateTime, nullable = False)
    location = Column(String, nullable = False)
    description = Column(String, nullable = False)

    ticket_types=relationship("TicketType", back_populates="event")

class TicketType(Base):
    __tablename__ = "ticket_types"

    id = Column(Integer, primary_key = True, index = True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable = False, index = True)
    price = Column(Integer, nullable = False)
    capacity = Column(Integer, nullable = False)
    
    event = relationship("Event", back_populates="ticket_types")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index = True)
    ticket_type_id = Column(Integer, ForeignKey("ticket_types.id"), nullable=False, index = True)
    quantity = Column(Integer, nullable = False)
    status = Column(String, nullable = False, default="booked")
    created_at = Column(DateTime, server_default=func.now())