import pathlib
#import time
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src import models, schemas
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from src.auth import hash_password, verify_password, create_access_token, get_current_user

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/register', response_model = schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed=hash_password(user.password)
    new_user = models.User(
        email=user.email,
        password=hashed,
        name=user.name,
        role="customer",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post('/login', response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not existing_user or not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code = 401, detail = "Invalid email or password")
    create_access_token(data = {"sub": existing_user.email})
    token = create_access_token(data = {"sub": existing_user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post('/events', response_model=schemas.EventOut)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create events")
    new_event=models.Event(
        name=event.name,
        event_date=event.event_date,
        location=event.location,
        description=event.description,
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    for ticket_type in event.ticket_types:
        new_ticket_type = models.TicketType(
            event_id=new_event.id,
            price = ticket_type.price,
            capacity=ticket_type.capacity,
        )
        db.add(new_ticket_type)

    db.commit()
    db.refresh(new_event)

    return new_event

@app.get('/events', response_model=list[schemas.EventOut])
def show_event(db: Session = Depends(get_db)):
    events=db.query(models.Event).all()
    return events

@app.post('/bookings', response_model =schemas.BookingOut)
def booking_create(booking: schemas.BookingCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    ticket_type = db.query(models.TicketType).filter(models.TicketType.id == booking.ticket_type_id).with_for_update().first()
    if not ticket_type:
        raise HTTPException(status_code=404, detail="Ticket type not found")

    existing_bookings = db.query(models.Booking).filter(
        models.Booking.ticket_type_id == booking.ticket_type_id,
        models.Booking.status == "booked"
    ).all()
    total_booked=sum(b.quantity for b in existing_bookings)
#    time.sleep(0.1) # artificial delay used to reliably reproduce the race condition during testing.

    if total_booked + booking.quantity > ticket_type.capacity:
        raise HTTPException(status_code = 409, detail = "Not enough capacity")
    
    new_booking = models.Booking(
    user_id=current_user.id,
    ticket_type_id=booking.ticket_type_id,
    quantity=booking.quantity,
    status="booked",
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@app.get('/bookings/{booking_id}', response_model=schemas.BookingOut)
def get_booking(booking_id: int, db: Session=Depends(get_db), current_user: models.User = Depends(get_current_user)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@app.patch('/bookings/{booking_id}/cancel', response_model=schemas.BookingOut)
def cancel_booking(booking_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking.status="cancelled"
    db.commit()
    db.refresh(booking)
    return booking