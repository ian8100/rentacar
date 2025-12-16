"""
Rental class for the car rental system.
Manages rental transactions and their lifecycle.
"""
from datetime import datetime, timedelta
try:
    from Vehicule import Car
    from Customer import Customer
except ImportError:
    pass
class Rental:
    """Represents a car rental transaction."""
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
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
            daily_penalty = self.vehicle.daily_rate * self.LATE_RETURN_PENALTY_PERCENT
            self.late_return_penalty = daily_penalty * late_days
            self.total_cost += self.late_return_penalty
        
        self.vehicle.increment_rental_count()
        
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
        return (f"Rental({self.rental_id}, customer={self.customer.customer_id}, "f"vehicle={self.vehicle.vehicle_id}, status={self.status})")

if __name__ == "__main__":
    print("🚀 Démarrage du test unitaire de la classe Rental...\n")

    try:
        mock_car = Car(1, "Peugeot", "208", "car", 40.0, 4, "Essence")
        mock_customer = Customer(1, "Alice", "Test", 25, "B")
        print(f"✅ Objets créés: {mock_car} | {mock_customer}")

        start = datetime.now()
        duration_days = 5
        end = start + timedelta(days=duration_days)

        print(f"\n--- Test Création (Durée: {duration_days} jours) ---")
        rental = Rental(101, mock_customer, mock_car, start, end)
        print(f"Status initial: {rental.status}")
        print(f"Coût initial attendu ({duration_days} * 40.0): {rental.total_cost}€")
        
        assert rental.total_cost == 200.0
        print("✅ Calcul du coût initial correct.")

        print("\n--- Test Extension (+2 jours) ---")
        new_end = end + timedelta(days=2)
        rental.extend_rental(new_end)
        print(f"Nouvelle date de fin: {rental.end_date}")
        print(f"Nouveau coût attendu (7 * 40.0): {rental.total_cost}€")
        
        assert rental.total_cost == 280.0
        print("✅ Calcul après extension correct.")

        print("\n--- Test Retour en retard (1 jour de retard) ---")
        actual_return = new_end + timedelta(days=1)
        
        rental.complete_rental(actual_return)
        
        print(f"Pénalité calculée: {rental.late_return_penalty}€")
        print(f"Coût final total: {rental.total_cost}€")
        print(f"Status final: {rental.status}")

        assert rental.late_return_penalty == 20.0
        assert rental.total_cost == 300.0
        print("✅ Calcul des pénalités correct.")

    except ImportError:
        print("❌ Impossible de lancer le test : Les fichiers Vehicule.py ou Customer.py sont introuvables.")
    except Exception as e:
        print(f"❌ Erreur durant le test: {e}")