"""
Customer class for the car rental system.
Manages customer information and rental history.
"""

from datetime import datetime
from enum import Enum


class LicenseType(Enum):
    """Enumeration for driver license types."""
    AUTO_LIGHT = "auto_light"  # Category B - cars
    AUTO_HEAVY = "auto_heavy"  # Category C - trucks
    MOTORCYCLE = "motorcycle"  # Category A


class Customer:
    """Represents a customer in the rental system."""
    
    def __init__(self, customer_id, first_name, last_name, age, license_type=LicenseType.AUTO_LIGHT):
        """
        Initialize a customer.
        
        Args:
            customer_id (int): Unique customer identifier
            first_name (str): Customer's first name
            last_name (str): Customer's last name
            age (int): Customer's age
            license_type (LicenseType): Type of driver's license
        """
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.license_type = license_type
        self.rental_history = []
        self.total_spent = 0.0
        self.registration_date = datetime.now()
        
    def get_full_name(self):
        """Return customer's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def add_rental_to_history(self, rental):
        """
        Add a rental to customer's history.
        
        Args:
            rental: Rental object to add to history
        """
        self.rental_history.append(rental)
        self.total_spent += rental.total_cost
        
    def get_rental_count(self):
        """Return the number of rentals for this customer."""
        return len(self.rental_history)
    
    def get_rental_history(self):
        """Return customer's rental history."""
        return self.rental_history.copy()
    
    def get_active_rentals(self):
        """Return only active (ongoing) rentals."""
        active = []
        for rental in self.rental_history:
            if rental.is_active():
                active.append(rental)
        return active
    
    def has_valid_license(self):
        """Check if customer has a valid license."""
        return self.license_type is not None
    
    def can_rent_vehicle(self, vehicle):
        """
        Check if customer can rent a specific vehicle.
        
        Args:
            vehicle: Vehicle object to check eligibility for
            
        Returns:
            bool: True if customer can rent this vehicle
        """
        # Check age requirement
        if not vehicle.is_eligible_for_customer(self.age):
            return False
        
        # Check license type matches vehicle type
        if vehicle.category in ['sedan', 'SUV', 'hatchback']:
            return self.license_type in [LicenseType.AUTO_LIGHT, LicenseType.AUTO_HEAVY]
        elif vehicle.category == 'truck':
            return self.license_type == LicenseType.AUTO_HEAVY
        elif vehicle.category in ['sport', 'cruiser', 'touring']:
            return self.license_type == LicenseType.MOTORCYCLE
        
        return False
    
    def get_discount_rate(self):
        """
        Calculate discount rate based on rental history.
        More rentals = higher discount.
        """
        rental_count = self.get_rental_count()
        if rental_count >= 20:
            return 0.15  # 15% discount
        elif rental_count >= 10:
            return 0.10  # 10% discount
        elif rental_count >= 5:
            return 0.05  # 5% discount
        else:
            return 0.0  # No discount
    
    def __str__(self):
        """String representation of customer."""
        return f"Customer {self.get_full_name()} (ID: {self.customer_id}) - Age: {self.age} - License: {self.license_type.value}"
    
    def __repr__(self):
        """Developer representation."""
        return f"Customer({self.customer_id}, '{self.first_name}', '{self.last_name}', {self.age}, {self.license_type})"
