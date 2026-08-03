from pydantic import BaseModel, EmailStr, constr, conint
from datetime import datetime

class TicketTypeCreate(BaseModel):
    price: conint(gt=0)
    capacity: conint(gt=0)

class TicketTypeOut(BaseModel):
    id: int
    price: int
    capacity: int

    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    name: constr(min_length=1)
    event_date: datetime
    location: constr(min_length=1)
    description: constr(min_length=1)
    ticket_types: list[TicketTypeCreate]

class EventOut(BaseModel):
    id: int
    name: str
    event_date: datetime
    location: str
    description: str
    ticket_types: list[TicketTypeOut]

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    name: constr(min_length=1)


class UserOut(BaseModel):
    id: int
    email: str
    name: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class BookingCreate(BaseModel):
    ticket_type_id: int
    quantity: int

class BookingOut(BaseModel):
    id: int
    user_id: int
    ticket_type_id: int
    quantity: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True