from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://user:password@localhost/dbname')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"

class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    description = Column(String)

    def __init__(self, name, address, description):
        self.name = name
        self.address = address
        self.description = description

    def __repr__(self):
        return f"Hotel('{self.name}', '{self.address}', '{self.description}')"

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    hotel_id = Column(Integer)
    checkin = Column(String)
    checkout = Column(String)

    def __init__(self, user_id, hotel_id, checkin, checkout):
        self.user_id = user_id
        self.hotel_id = hotel_id
        self.checkin = checkin
        self.checkout = checkout

    def __repr__(self):
        return f"Booking('{self.user_id}', '{self.hotel_id}', '{self.checkin}', '{self.checkout}')"

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()