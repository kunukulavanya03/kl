from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi import status
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

class User(BaseModel):
    username: str
    email: str
    password: str

class Hotel(BaseModel):
    name: str
    address: str
    description: str

class Booking(BaseModel):
    user_id: int
    hotel_id: int
    checkin: str
    checkout: str

engine = create_engine('postgresql://user:password@localhost/dbname')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

@app.post("/api/register")
def register(user: User):
    new_user = User(username=user.username, email=user.email, password=user.password)
    session.add(new_user)
    session.commit()
    return {"message": "User created successfully"}

@app.post("/api/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = session.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    if not user.password == form_data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    access_token = jwt.encode({"sub": user.username}, "secret_key", algorithm="HS256")
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/profile")
def profile(token: str = Depends()):
    user = session.query(User).filter(User.username == token).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"id": user.id, "username": user.username, "email": user.email}

@app.put("/api/profile")
def update_profile(user: User, token: str = Depends()):
    user_to_update = session.query(User).filter(User.username == token).first()
    if not user_to_update:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_to_update.username = user.username
    user_to_update.email = user.email
    session.commit()
    return {"message": "Profile updated successfully"}

@app.delete("/api/profile")
def delete_profile(token: str = Depends()):
    user_to_delete = session.query(User).filter(User.username == token).first()
    if not user_to_delete:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    session.delete(user_to_delete)
    session.commit()
    return {"message": "Profile deleted successfully"}

@app.post("/api/hotels")
def create_hotel(hotel: Hotel):
    new_hotel = Hotel(name=hotel.name, address=hotel.address, description=hotel.description)
    session.add(new_hotel)
    session.commit()
    return {"message": "Hotel created successfully"}

@app.get("/api/hotels")
def get_hotels():
    hotels = session.query(Hotel).all()
    return [{"id": hotel.id, "name": hotel.name, "address": hotel.address, "description": hotel.description} for hotel in hotels]

@app.get("/api/hotels/{hotel_id}")
def get_hotel(hotel_id: int):
    hotel = session.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    return {"id": hotel.id, "name": hotel.name, "address": hotel.address, "description": hotel.description}

@app.put("/api/hotels/{hotel_id}")
def update_hotel(hotel: Hotel, hotel_id: int):
    hotel_to_update = session.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    hotel_to_update.name = hotel.name
    hotel_to_update.address = hotel.address
    hotel_to_update.description = hotel.description
    session.commit()
    return {"message": "Hotel updated successfully"}

@app.delete("/api/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    hotel_to_delete = session.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    session.delete(hotel_to_delete)
    session.commit()
    return {"message": "Hotel deleted successfully"}

@app.post("/api/bookings")
def create_booking(booking: Booking):
    new_booking = Booking(user_id=booking.user_id, hotel_id=booking.hotel_id, checkin=booking.checkin, checkout=booking.checkout)
    session.add(new_booking)
    session.commit()
    return {"message": "Booking created successfully"}

@app.get("/api/bookings")
def get_bookings():
    bookings = session.query(Booking).all()
    return [{"id": booking.id, "user_id": booking.user_id, "hotel_id": booking.hotel_id, "checkin": booking.checkin, "checkout": booking.checkout} for booking in bookings]

@app.get("/api/bookings/{booking_id}")
def get_booking(booking_id: int):
    booking = session.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return {"id": booking.id, "user_id": booking.user_id, "hotel_id": booking.hotel_id, "checkin": booking.checkin, "checkout": booking.checkout}

@app.put("/api/bookings/{booking_id}")
def update_booking(booking: Booking, booking_id: int):
    booking_to_update = session.query(Booking).filter(Booking.id == booking_id).first()
    if not booking_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    booking_to_update.user_id = booking.user_id
    booking_to_update.hotel_id = booking.hotel_id
    booking_to_update.checkin = booking.checkin
    booking_to_update.checkout = booking.checkout
    session.commit()
    return {"message": "Booking updated successfully"}

@app.delete("/api/bookings/{booking_id}")
def delete_booking(booking_id: int):
    booking_to_delete = session.query(Booking).filter(Booking.id == booking_id).first()
    if not booking_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    session.delete(booking_to_delete)
    session.commit()
    return {"message": "Booking deleted successfully"}
