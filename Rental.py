"""
Rental class for the car rental system.
Manages rental transactions and their lifecycle.
"""

from datetime import datetime, timedelta
from enum import Enum


class RentalStatus(Enum):
    """Enumeration for rental status."""
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Rental:
    """Represents a car rental transaction."""
    
    LATE_RETURN_PENALTY_PERCENT = 0.50  # 50% penalty per day
    
    def __init__(self, rental_id, customer, vehicle, start_date, end_date):
        """
        Initialize a rental.
        
        Args:
            rental_id (int): Unique rental identifier
            customer: Customer object
            vehicle: Vehicle object
            start_date (datetime): Start date of rental
            end_date (datetime): End date of rental
        """
        if end_date <= start_date:
            raise ValueError("End date must be after start date")
        
        self.rental_id = rental_id
        self.customer = customer
        self.vehicle = vehicle
        self.start_date = start_date
        self.end_date = end_date
        self.actual_return_date = None
        self.status = RentalStatus.ACTIVE
        self.creation_date = datetime.now()
        self.total_cost = self._calculate_total_cost()
        self.late_return_penalty = 0.0
        
    def _calculate_total_cost(self):
        """Calculate the total cost of the rental."""
        duration = (self.end_date - self.start_date).days
        if duration == 0:
            duration = 1  # Minimum 1 day rental
        
        base_cost = self.vehicle.daily_rate * duration
        
        # Apply customer discount
        discount_rate = self.customer.get_discount_rate()
        discount = base_cost * discount_rate
        
        return base_cost - discount
    
    def complete_rental(self, actual_return_date=None):
        """
        Complete the rental and calculate final cost.
        
        Args:
            actual_return_date (datetime): Actual return date. If None, uses planned end_date.
        """
        if actual_return_date is None:
            actual_return_date = datetime.now()
        
        self.actual_return_date = actual_return_date
        self.status = RentalStatus.COMPLETED
        
        # Calculate late return penalty
        if actual_return_date > self.end_date:
            late_days = (actual_return_date - self.end_date).days
            daily_penalty = self.vehicle.daily_rate * self.LATE_RETURN_PENALTY_PERCENT
            self.late_return_penalty = daily_penalty * late_days
            self.total_cost += self.late_return_penalty
        
        # Update vehicle
        self.vehicle.increment_rental_count()
        self.vehicle.set_state(self.vehicle.state.__class__.AVAILABLE)
        
        # Update customer
        self.customer.add_rental_to_history(self)
    
    def cancel_rental(self):
        """Cancel the rental."""
        if self.status == RentalStatus.COMPLETED:
            raise ValueError("Cannot cancel a completed rental")
        
        self.status = RentalStatus.CANCELLED
        self.total_cost = 0  # No charge for cancelled rental
    
    def is_active(self):
        """Check if rental is currently active."""
        return self.status == RentalStatus.ACTIVE
    
    def is_overdue(self):
        """Check if rental is overdue (returns True if return date has passed)."""
        if self.status != RentalStatus.ACTIVE:
            return False
        return datetime.now() > self.end_date
    
    def get_remaining_days(self):
        """Get remaining days until end date."""
        if self.status != RentalStatus.ACTIVE:
            return 0
        remaining = (self.end_date - datetime.now()).days
        return max(0, remaining)
    
    def extend_rental(self, new_end_date):
        """
        Extend the rental to a new end date.
        
        Args:
            new_end_date (datetime): New end date
        """
        if self.status != RentalStatus.ACTIVE:
            raise ValueError("Can only extend active rentals")
        
        if new_end_date <= self.end_date:
            raise ValueError("New end date must be after current end date")
        
        self.end_date = new_end_date
        self.total_cost = self._calculate_total_cost()
    
    def get_rental_duration_days(self):
        """Get the rental duration in days."""
        duration = (self.end_date - self.start_date).days
        return max(1, duration)
    
    def __str__(self):
        """String representation of rental."""
        return (f"Rental {self.rental_id}: {self.customer.get_full_name()} - "
                f"{self.vehicle.brand} {self.vehicle.model} - "
                f"${self.total_cost:.2f} - Status: {self.status.value}")
    
    def __repr__(self):
        """Developer representation."""
        return (f"Rental({self.rental_id}, customer={self.customer.customer_id}, "
                f"vehicle={self.vehicle.vehicle_id}, status={self.status})")
