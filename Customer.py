
"""
Customer class for the car rental system.
Manages customer information and rental history.
"""
from datetime import datetime

class Customer:
    """Represents a customer in the rental system."""
    CAR = "B"  # Category B - cars
    TRUCK = "C"  # Category C - trucks
    MOTORCYCLE = "A"  # Category A - motorcycles

    def __init__(self, customer_id: int, first_name: str, last_name: str, age: int, license_type: str):
        """
        Initialize a customer.
        
        Args:
            customer_id (int): Unique customer identifier
            first_name (str): Customer's first name
            last_name (str): Customer's last name
            age (int): Customer's age
            license_type (str): Type of driver's license
        """
        self.customer_id: int = customer_id
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.age: int = age
        self.license_type: str = license_type
        self.rental_history: list = []
        self.total_spent: float = 0.0
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
        if not vehicle.is_eligible_for_customer(self.age):
            return False
        
        if vehicle.category in ['car', 'van']:
            return self.license_type in [self.CAR, self.TRUCK]
        elif vehicle.category == 'truck':
            return self.license_type == self.TRUCK
        elif vehicle.category in ['bike', 'scooter']:
            return self.license_type == self.MOTORCYCLE
        
        return False
        
    def __str__(self):
        """String representation of customer."""
        return f"Customer {self.get_full_name()} (ID: {self.customer_id}) - Age: {self.age} - License: {self.license_type}"
    
    def __repr__(self):
        """Developer representation."""
        return f"Customer({self.customer_id}, '{self.first_name}', '{self.last_name}', {self.age}, {self.license_type})"
