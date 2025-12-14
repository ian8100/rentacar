"""
Rental class for the car rental system.
Manages rental transactions and their lifecycle.
"""
from datetime import datetime, timedelta

class Rental:
    """Represents a car rental transaction."""
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    # CORRECTION 1 : Ajout de la constante manquante
    LATE_RETURN_PENALTY_PERCENT = 0.5
    
    def __init__(self, rental_id: int, customer, vehicle, start_date: datetime, end_date: datetime):
        """
        Initialize a rental.
        """
        if end_date <= start_date:
            raise ValueError("End date must be after start date")
        
        self.rental_id: int = rental_id
        self.customer = customer
        self.vehicle = vehicle
        self.start_date: datetime = start_date
        self.end_date: datetime = end_date
        self.actual_return_date = None
        self.status = self.ACTIVE
        self.creation_date: datetime = datetime.now()
        self.total_cost: float = self._calculate_total_cost()
        self.late_return_penalty: float = 0.0
        
    def _calculate_total_cost(self):
        """Calculate the total cost of the rental."""
        duration = (self.end_date - self.start_date).days
        if duration == 0:
            duration = 1          
        return self.vehicle.daily_rate * duration
    
    def complete_rental(self, actual_return_date=None):
        """
        Complete the rental and calculate final cost.
        """
        if actual_return_date is None:
            actual_return_date = datetime.now()
        
        self.actual_return_date = actual_return_date
        self.status = self.COMPLETED
        
        if actual_return_date > self.end_date:
            late_days = (actual_return_date - self.end_date).days
            # Utilisation de la constante définie plus haut
            daily_penalty = self.vehicle.daily_rate * self.LATE_RETURN_PENALTY_PERCENT
            self.late_return_penalty = daily_penalty * late_days
            self.total_cost += self.late_return_penalty
        
        self.vehicle.increment_rental_count()
        
        # CORRECTION 2 : Correction de l'accès à la constante AVAILABLE
        # Au lieu de passer par l'état (str), on passe par l'objet véhicule
        self.vehicle.set_state(self.vehicle.AVAILABLE)
        
        self.customer.add_rental_to_history(self)
    
    def cancel_rental(self):
        """Cancel the rental."""
        if self.status == self.COMPLETED:
            raise ValueError("Cannot cancel a completed rental")
        
        self.status = self.CANCELLED
        self.total_cost = 0  
    
    def is_active(self):
        """Check if rental is currently active."""
        return self.status == self.ACTIVE
    
    def is_overdue(self):
        """Check if rental is overdue."""
        if self.status != self.ACTIVE:
            return False
        return datetime.now() > self.end_date
    
    def get_remaining_days(self):
        """Get remaining days until end date."""
        if self.status != self.ACTIVE:
            return 0
        remaining = (self.end_date - datetime.now()).days
        return max(0, remaining)
    
    def extend_rental(self, new_end_date: datetime):
        """Extend the rental to a new end date."""
        if self.status != self.ACTIVE:
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
        return (f"Rental {self.rental_id}: {self.customer.get_full_name()} - "
                f"{self.vehicle.brand} {self.vehicle.model} - "
                f"${self.total_cost:.2f} - Status: {self.status}")
    
    def __repr__(self):
        return (f"Rental({self.rental_id}, customer={self.customer.customer_id}, "
<<<<<<< HEAD
                f"vehicle={self.vehicle.vehicle_id}, status={self.status})")
=======
                f"vehicle={self.vehicle.vehicle_id}, status={self.status})")
>>>>>>> f198589ef84f82d7c049cc6e30791f77e973f22b
