from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Vehicule(ABC):
    """Abstract base class for all vehicles."""
    AVAILABLE: str = "available"
    RENTED: str = "rented"
    MAINTENANCE: str = "maintenance"
    RESERVED: str = "reserved"
    
    def __init__(self, vehicle_id: int, brand: str, model: str, category: str, daily_rate: float):
        """
        Initialize a vehicle.
        
        Args:
            vehicle_id (int): Unique vehicle identifier
            brand (str): Vehicle brand
            model (str): Vehicle model
            category (str): Vehicle category
            daily_rate (float): Daily rental rate
            state (str): Initial state of the vehicle
        """
        self.vehicle_id: int = vehicle_id
        self.brand: str = brand
        self.model: str = model
        self.category: str = category
        self.daily_rate: float = daily_rate
        self.state: str = self.AVAILABLE
        self.maintenance_history: list = []
        self.rental_count: int = 0
        
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
        if self.state == self.RENTED:
            raise ValueError(f"Cannot schedule maintenance for {self.vehicle_id}: vehicle is currently rented")
        
        maintenance_record = {
            'date': datetime.now(),
            'description': description,
            'estimated_days': estimated_days,
            'completed': False
        }
        self.maintenance_history.append(maintenance_record)
        self.state = self.MAINTENANCE
        
    def complete_maintenance(self):
        """Mark the last maintenance as completed and set vehicle to available."""
        if self.maintenance_history:
            self.maintenance_history[-1]['completed'] = True
            self.maintenance_history[-1]['completion_date'] = datetime.now()
        self.state = self.AVAILABLE
        
    def is_available(self):
        """Check if vehicle is available for rent."""
        return self.state == self.AVAILABLE
    
    def set_state(self, new_state):
        """Update vehicle state."""
        self.state = new_state
        
    def increment_rental_count(self):
        """Increment the rental counter."""
        self.rental_count += 1
    
    def __str__(self):
        """String representation of the vehicle."""
        return f"{self.brand} {self.model} ({self.vehicle_id}) - {self.daily_rate}€/day - {self.state}"
    
    def __repr__(self):
        """Developer representation of the vehicle."""
        return f"{self.__class__.__name__}({self.vehicle_id}, '{self.brand}', '{self.model}', '{self.category}', {self.daily_rate})"


class Car(Vehicule):
    """Represents a car."""
    
    MIN_AGE: int = 17
    AVAILABLE: str = "available"
    RENTED: str = "rented"
    MAINTENANCE: str = "maintenance"
    RESERVED: str = "reserved"
    
    def __init__(self, vehicle_id: int, brand: str, model: str, category: str, daily_rate: float, num_doors: int, fuel_type: str):
        """
        Initialize a car.
        
        Args:
            vehicle_id (int): Unique vehicle identifier
            brand (str): Vehicle brand
            model (str): Vehicle model
            category (str): Car category
            daily_rate (float): Daily rental rate
            num_doors (int): Number of doors
            fuel_type (str): Type of fuel (petrol, diesel, electric, hybrid)
            state (str): Initial state
        """
        super().__init__(vehicle_id, brand, model, category, daily_rate)
        self.state: str = self.AVAILABLE
        self.num_doors: int = num_doors
        self.fuel_type: int = fuel_type
        
    def get_description(self):
        """Return car description."""
        return f"{self.brand} {self.model} - {self.category} ({self.num_doors}-door, {self.fuel_type})"
    
    def is_eligible_for_customer(self, customer_age):
        """Check if customer meets age requirement (18+)."""
        return customer_age >= self.MIN_AGE
    
    def __str__(self):
        """String representation."""
        return f"Car: {super().__str__()} | {self.fuel_type} | {self.num_doors} doors"


class Truck(Vehicule):
    """Represents a truck for commercial use."""
    
    MIN_AGE: int = 21  
    AVAILABLE: str = "available"
    RENTED: str = "rented"
    MAINTENANCE: str = "maintenance"
    RESERVED: str = "reserved"
    
    def __init__(self, vehicle_id: int, brand: str, model: str, category: str, daily_rate: float, payload_capacity: float):
        """
        Initialize a truck.
        
        Args:
            vehicle_id (int): Unique vehicle identifier
            brand (str): Vehicle brand
            model (str): Vehicle model
            category (str): Truck category
            daily_rate (float): Daily rental rate
            payload_capacity (float): Payload capacity in tons
            state (str): Initial state
        """
        super().__init__(vehicle_id, brand, model, category, daily_rate)
        self.state: str = self.AVAILABLE
        self.payload_capacity: float = payload_capacity
        
    def get_description(self):
        """Return truck description."""
        return f"{self.brand} {self.model} - Payload: {self.payload_capacity}T"
    
    def is_eligible_for_customer(self, customer_age: int):
        """Check if customer meets age requirement (21+)."""
        return customer_age >= self.MIN_AGE
    
    def __str__(self):
        """String representation."""
        return f"Truck: {super().__str__()} | Capacity: {self.payload_capacity}T"


class Motorcycle(Vehicule):
    """Represents a motorcycle."""
    
    MIN_AGE: int = 18 
    AVAILABLE: str = "available"
    RENTED: str = "rented"
    MAINTENANCE: str = "maintenance"
    RESERVED: str = "reserved"
    
    def __init__(self, vehicle_id: int, brand: str, model: str, category: str, daily_rate: float, engine_cc: int):
        """
        Initialize a motorcycle.
        
        Args:
            vehicle_id (int): Unique vehicle identifier
            brand (str): Vehicle brand
            model (str): Vehicle model
            category (str): Motorcycle category (sport, cruiser, touring)
            daily_rate (float): Daily rental rate
            engine_cc (int): Engine displacement in cubic centimeters
            state (str): Initial state
        """
        super().__init__(vehicle_id, brand, model, category, daily_rate)
        self.state: str = self.AVAILABLE
        self.engine_cc = engine_cc
        
    def get_description(self):
        """Return motorcycle description."""
        return f"{self.brand} {self.model} - {self.engine_cc}cc {self.category}"
    
    def is_eligible_for_customer(self, customer_age: int):
        """Check if customer meets age requirement (18+)."""
        return customer_age >= self.MIN_AGE
    
    def __str__(self):
        """String representation."""
        return f"Motorcycle: {super().__str__()} | {self.engine_cc}cc"

if __name__ == "__main__":
    print("🚗 Démarrage du test unitaire des classes Véhicule...\n")

    try:
        car = Car(1, "Fiat", "500", "car", 35.0, 2, "Essence")
        truck = Truck(2, "Mercedes", "Actros", "truck", 120.0, 18.0)
        moto = Motorcycle(3, "Kawasaki", "Ninja", "sport", 90.0, 1000)
        
        vehicles = [car, truck, moto]
        
        print("--- 1. Test d'Affichage (__str__) ---")
        for v in vehicles:
            print(f"✅ {v}")

    except Exception as e:
        print(f"❌ Erreur de création : {e}")

    print("\n--- 2. Test Descriptions ---")
    for v in vehicles:
        print(f"ℹ️  {v.get_description()}")

    print("\n--- 3. Test Éligibilité (Age) ---")
    age_jeune = 19
    print(f"Conducteur de {age_jeune} ans :")
    print(f" - Peut louer Car (Min 17)? {'✅ OUI' if car.is_eligible_for_customer(age_jeune) else '❌ NON'}")
    print(f" - Peut louer Truck (Min 21)? {'✅ OUI' if truck.is_eligible_for_customer(age_jeune) else '❌ NON'}")
    print(f" - Peut louer Moto (Min 18)? {'✅ OUI' if moto.is_eligible_for_customer(age_jeune) else '❌ NON'}")

    print("\n--- 4. Test Cycle Maintenance ---")
    print(f"État initial Moto: {moto.state}")
    print(">>> Envoi en maintenance...")
    moto.schedule_maintenance("Vidange moteur", 1)
    
    if moto.state == Vehicule.MAINTENANCE and not moto.is_available():
        print(f"✅ Moto bien passée en maintenance : {moto.state}")
    else:
        print(f"❌ Erreur état maintenance : {moto.state}")
        
    print(">>> Fin de maintenance...")
    moto.complete_maintenance()
    
    if moto.is_available():
        print(f"✅ Moto de nouveau disponible : {moto.state}")
    else:
        print(f"❌ Erreur fin maintenance : {moto.state}")