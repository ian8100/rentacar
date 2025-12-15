# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class DBVehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String)
    model = Column(String)
    category = Column(String) # car, truck, bike
    daily_rate = Column(Float)
    state = Column(String, default="available")
    
    # Champs spécifiques (nullable car dépendent du type)
    num_doors = Column(Integer, nullable=True)
    fuel_type = Column(String, nullable=True)
    payload_capacity = Column(Float, nullable=True)
    engine_cc = Column(Integer, nullable=True)

    # Relation avec les locations
    rentals = relationship("DBRental", back_populates="vehicle")

class DBCustomer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    license_type = Column(String)

    rentals = relationship("DBRental", back_populates="customer")

class DBRental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    actual_return_date = Column(DateTime, nullable=True)
    status = Column(String, default="active")
    total_cost = Column(Float, default=0.0)
    penalty = Column(Float, default=0.0)

    # Relations pour pouvoir faire rental.customer ou rental.vehicle
    customer = relationship("DBCustomer", back_populates="rentals")
    vehicle = relationship("DBVehicle", back_populates="rentals")