
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

if __name__ == "__main__":
    print("👤 Démarrage du test unitaire de la classe Customer...\n")

    class MockVehicle:
        def __init__(self, category, is_age_ok=True):
            self.category = category
            self.is_age_ok = is_age_ok 
        
        def is_eligible_for_customer(self, age):
            return self.is_age_ok

    class MockRental:
        def __init__(self, cost, active=True):
            self.total_cost = cost
            self._active = active
        def is_active(self): return self._active
        def __repr__(self): return f"Rental({self.total_cost}€)"

    print("--- 1. Création de clients ---")
    c_voiture = Customer(1, "Alice", "Dupont", 25, "B") 
    c_camion = Customer(2, "Bob", "Builder", 40, "C")   
    c_moto = Customer(3, "Charlie", "Biker", 20, "A")   
    c_jeune = Customer(4, "Junior", "Doe", 14, "B")     

    print(f"✅ {c_voiture}")
    print(f"✅ {c_moto}")
    print(f"✅ {c_camion}")
    print(f"✅ {c_jeune}")

    print("\n--- 2. Test Eligibilité ---")
    
    v_car = MockVehicle("car")
    v_truck = MockVehicle("truck")
    v_moto = MockVehicle("bike")
    v_strict = MockVehicle("car", is_age_ok=False) 

    can_rent = c_voiture.can_rent_vehicle(v_car)
    print(f"Permis B loue Voiture ? {'✅ OUI' if can_rent else '❌ NON'}")

    can_rent = c_voiture.can_rent_vehicle(v_truck)
    print(f"Permis B loue Camion ? {'❌ NON' if not can_rent else '✅ OUI'}")

    can_rent = c_camion.can_rent_vehicle(v_truck)
    print(f"Permis C loue Camion ? {'✅ OUI' if can_rent else '❌ NON'}")

    can_rent = c_jeune.can_rent_vehicle(v_strict) 
    print(f"Junior (14 ans) loue Voiture ? {'❌ NON' if not can_rent else '✅ OUI'}")

    print("\n--- 3. Test Historique & Dépenses ---")
    r1 = MockRental(100.0, active=False) 
    r2 = MockRental(250.50, active=True) 

    c_voiture.add_rental_to_history(r1)
    c_voiture.add_rental_to_history(r2)

    print(f"Nombre de locations: {c_voiture.get_rental_count()} (Attendu: 2)")
    print(f"Total dépensé: {c_voiture.total_spent}€ (Attendu: 350.5)")
    
    active_rentals = c_voiture.get_active_rentals()
    print(f"Locations actives: {len(active_rentals)} (Attendu: 1)")

    if c_voiture.total_spent == 350.5 and len(active_rentals) == 1:
        print("✅ Gestion de l'historique validée.")
    else:
        print("❌ Erreur dans l'historique.")