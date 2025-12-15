from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class VehicleCreate(BaseModel):
    brand: str
    model: str
    category: str
    daily_rate: float

    num_doors: Optional[int] = 4
    fuel_type: Optional[str] = "petrol"
    payload_capacity: Optional[float] = None
    engine_cc: Optional[int] = None

class VehicleResponse(BaseModel):
    vehicle_id: int
    brand: str
    model: str
    category: str
    daily_rate: float
    state: str

class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    license_type: str

class CustomerResponse(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    license_type: str

class RentalCreate(BaseModel):
    customer_id: int
    vehicle_id: int
    start_date: datetime
    end_date: datetime

class RentalResponse(BaseModel):
    rental_id: int
    status: str
    total_cost: float
