"""
Vehicle hierarchy for the car rental system.
Classes: Vehicle (abstract), Car, Truck, Motorcycle
"""

from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime


class VehicleState(Enum):
    """Enumeration for vehicle states."""
    AVAILABLE = "available"
    RENTED = "rented"
    MAINTENANCE = "maintenance"
    RESERVED = "reserved"


class Vehicle(ABC):
    """Abstract base class for all vehicles."""
    
    def __init__(self, vehicle_id, brand, model, category, daily_rate, state=VehicleState.AVAILABLE):
        """
        Initialize a vehicle.
        
        Args:
            vehicle_id (int): Unique vehicle identifier
            brand (str): Vehicle brand
            model (str): Vehicle model
            category (str): Vehicle category
            daily_rate (float): Daily rental rate
            state (VehicleState): Initial state of the vehicle
        """
        self.vehicle_id = vehicle_id
        self.brand = brand
        self.model = model
        self.category = category
        self.daily_rate = daily_rate
        self.state = state
        self.maintenance_history = []
        self.rental_count = 0
        
    @abstractmethod
    def get_description(self):
        """Return a description of the vehicle."""
        pass
    
    @abstractmethod
    def is_eligible_for_customer(self, customer_age):
        """Check if customer meets age requirements for this vehicle."""
        pass
    
    def schedule_maintenance(self, description, estimated_days=1):
        """
        Schedule maintenance for the vehicle.
        
        Args:
            description (str): Description of maintenance
            estimated_days (int): Estimated days for maintenance
        """
        if self.state == VehicleState.RENTED:
            raise ValueError(f"Cannot schedule maintenance for {self.vehicle_id}: vehicle is currently rented")
        
        maintenance_record = {
            'date': datetime.now(),
            'description': description,
            'estimated_days': estimated_days,
            'completed': False
        }
        self.maintenance_history.append(maintenance_record)
        self.state = VehicleState.MAINTENANCE
        
    def complete_maintenance(self):
        """Mark the last maintenance as completed and set vehicle to available."""
        if self.maintenance_history:
            self.maintenance_history[-1]['completed'] = True
            self.maintenance_history[-1]['completion_date'] = datetime.now()
        self.state = VehicleState.AVAILABLE
        
    def is_available(self):
        """Check if vehicle is available for rent."""
        return self.state == VehicleState.AVAILABLE
    
    def set_state(self, new_state):
        """Update vehicle state."""
        self.state = new_state
        
    def increment_rental_count(self):
        """Increment the rental counter."""
        self.rental_count += 1
    
    def __str__(self):
        """String representation of the vehicle."""
        return f"{self.brand} {self.model} ({self.vehicle_id}) - ${self.daily_rate}/day - {self.state.value}"
    
    def __repr__(self):
        """Developer representation of the vehicle."""
        return f"{self.__class__.__name__}({self.vehicle_id}, '{self.brand}', '{self.model}', '{self.category}', {self.daily_rate})"


class Car(Vehicle):
    """Represents a car (sedan, SUV, hatchback)."""
    
    MIN_AGE = 18
    
    def __init__(self, vehicle_id, brand, model, category, daily_rate, num_doors, fuel_type, state=VehicleState.AVAILABLE):
        """
        Initialize a car.
        
        Args:
            vehicle_id (int): Unique vehicle identifier
            brand (str): Vehicle brand
            model (str): Vehicle model
            category (str): Car category (sedan, SUV, hatchback)
            daily_rate (float): Daily rental rate
            num_doors (int): Number of doors
            fuel_type (str): Type of fuel (petrol, diesel, electric, hybrid)
            state (VehicleState): Initial state
        """
        super().__init__(vehicle_id, brand, model, category, daily_rate, state)
        self.num_doors = num_doors
        self.fuel_type = fuel_type
        
    def get_description(self):
        """Return car description."""
        return f"{self.brand} {self.model} - {self.category} ({self.num_doors}-door, {self.fuel_type})"
    
    def is_eligible_for_customer(self, customer_age):
        """Check if customer meets age requirement (18+)."""
        return customer_age >= self.MIN_AGE
    
    def __str__(self):
        """String representation."""
        return f"Car: {super().__str__()} | {self.fuel_type} | {self.num_doors} doors"


class Truck(Vehicle):
    """Represents a truck for commercial use."""
    
    MIN_AGE = 21  # Trucks require higher age
    
    def __init__(self, vehicle_id, brand, model, category, daily_rate, payload_capacity, state=VehicleState.AVAILABLE):
        """
        Initialize a truck.
        
        Args:
            vehicle_id (int): Unique vehicle identifier
            brand (str): Vehicle brand
            model (str): Vehicle model
            category (str): Truck category
            daily_rate (float): Daily rental rate
            payload_capacity (float): Payload capacity in tons
            state (VehicleState): Initial state
        """
        super().__init__(vehicle_id, brand, model, category, daily_rate, state)
        self.payload_capacity = payload_capacity
        
    def get_description(self):
        """Return truck description."""
        return f"{self.brand} {self.model} - Payload: {self.payload_capacity}T"
    
    def is_eligible_for_customer(self, customer_age):
        """Check if customer meets age requirement (21+)."""
        return customer_age >= self.MIN_AGE
    
    def __str__(self):
        """String representation."""
        return f"Truck: {super().__str__()} | Capacity: {self.payload_capacity}T"


class Motorcycle(Vehicle):
    """Represents a motorcycle."""
    
    MIN_AGE = 18  # Motorcycles require 18+ but with valid license
    
    def __init__(self, vehicle_id, brand, model, category, daily_rate, engine_cc, state=VehicleState.AVAILABLE):
        """
        Initialize a motorcycle.
        
        Args:
            vehicle_id (int): Unique vehicle identifier
            brand (str): Vehicle brand
            model (str): Vehicle model
            category (str): Motorcycle category (sport, cruiser, touring)
            daily_rate (float): Daily rental rate
            engine_cc (int): Engine displacement in cubic centimeters
            state (VehicleState): Initial state
        """
        super().__init__(vehicle_id, brand, model, category, daily_rate, state)
        self.engine_cc = engine_cc
        
    def get_description(self):
        """Return motorcycle description."""
        return f"{self.brand} {self.model} - {self.engine_cc}cc {self.category}"
    
    def is_eligible_for_customer(self, customer_age):
        """Check if customer meets age requirement (18+)."""
        return customer_age >= self.MIN_AGE
    
    def __str__(self):
        """String representation."""
        return f"Motorcycle: {super().__str__()} | {self.engine_cc}cc"
