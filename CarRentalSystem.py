"""
Car Rental System - Central management system
Manages vehicles, customers, rentals, and generates reports.
"""

from datetime import datetime, timedelta
from Vehicule import Vehicle, Car, Truck, Motorcycle, VehicleState
from Customer import Customer, LicenseType
from Rental import Rental, RentalStatus


class CarRentalSystem:
    """Central management system for car rental operations."""
    
    def __init__(self):
        """Initialize the car rental system."""
        self.vehicles = {}  # {vehicle_id: Vehicle}
        self.customers = {}  # {customer_id: Customer}
        self.rentals = {}  # {rental_id: Rental}
        self.next_vehicle_id = 1
        self.next_customer_id = 1
        self.next_rental_id = 1
        
    # ==================== VEHICLE MANAGEMENT ====================
    
    def add_vehicle(self, brand, model, category, daily_rate, **kwargs):
        """
        Add a vehicle to the fleet.
        
        Args:
            brand (str): Vehicle brand
            model (str): Vehicle model
            category (str): Vehicle category
            daily_rate (float): Daily rental rate
            **kwargs: Additional parameters depending on vehicle type
            
        Returns:
            Vehicle: The created vehicle
        """
        vehicle_id = self.next_vehicle_id
        self.next_vehicle_id += 1
        
        # Determine vehicle type and create appropriate object
        if category in ['sedan', 'SUV', 'hatchback']:
            vehicle = Car(
                vehicle_id, brand, model, category, daily_rate,
                kwargs.get('num_doors', 4),
                kwargs.get('fuel_type', 'petrol')
            )
        elif category == 'truck':
            vehicle = Truck(
                vehicle_id, brand, model, category, daily_rate,
                kwargs.get('payload_capacity', 5.0)
            )
        elif category in ['sport', 'cruiser', 'touring']:
            vehicle = Motorcycle(
                vehicle_id, brand, model, category, daily_rate,
                kwargs.get('engine_cc', 600)
            )
        else:
            raise ValueError(f"Unknown vehicle category: {category}")
        
        self.vehicles[vehicle_id] = vehicle
        return vehicle
    
    def remove_vehicle(self, vehicle_id):
        """
        Remove a vehicle from the fleet.
        
        Args:
            vehicle_id (int): ID of vehicle to remove
            
        Raises:
            ValueError: If vehicle not found or is currently rented
        """
        if vehicle_id not in self.vehicles:
            raise ValueError(f"Vehicle {vehicle_id} not found")
        
        vehicle = self.vehicles[vehicle_id]
        if vehicle.state == VehicleState.RENTED:
            raise ValueError(f"Cannot remove vehicle {vehicle_id}: currently rented")
        
        del self.vehicles[vehicle_id]
    
    def get_vehicle(self, vehicle_id):
        """Get a vehicle by ID."""
        if vehicle_id not in self.vehicles:
            raise ValueError(f"Vehicle {vehicle_id} not found")
        return self.vehicles[vehicle_id]
    
    def get_all_vehicles(self):
        """Get all vehicles in the fleet."""
        return list(self.vehicles.values())
    
    def get_available_vehicles(self):
        """Get all available vehicles."""
        return [v for v in self.vehicles.values() if v.is_available()]
    
    def get_vehicles_by_category(self, category):
        """Get vehicles by category."""
        return [v for v in self.vehicles.values() if v.category == category]
    
    def schedule_vehicle_maintenance(self, vehicle_id, description, estimated_days=1):
        """Schedule maintenance for a vehicle."""
        vehicle = self.get_vehicle(vehicle_id)
        vehicle.schedule_maintenance(description, estimated_days)
    
    def complete_vehicle_maintenance(self, vehicle_id):
        """Complete maintenance for a vehicle."""
        vehicle = self.get_vehicle(vehicle_id)
        vehicle.complete_maintenance()
    
    # ==================== CUSTOMER MANAGEMENT ====================
    
    def add_customer(self, first_name, last_name, age, license_type=LicenseType.AUTO_LIGHT):
        """
        Add a new customer.
        
        Args:
            first_name (str): Customer's first name
            last_name (str): Customer's last name
            age (int): Customer's age
            license_type (LicenseType): Type of driver's license
            
        Returns:
            Customer: The created customer
        """
        customer_id = self.next_customer_id
        self.next_customer_id += 1
        
        customer = Customer(customer_id, first_name, last_name, age, license_type)
        self.customers[customer_id] = customer
        return customer
    
    def remove_customer(self, customer_id):
        """
        Remove a customer.
        
        Args:
            customer_id (int): ID of customer to remove
            
        Raises:
            ValueError: If customer not found
        """
        if customer_id not in self.customers:
            raise ValueError(f"Customer {customer_id} not found")
        
        del self.customers[customer_id]
    
    def get_customer(self, customer_id):
        """Get a customer by ID."""
        if customer_id not in self.customers:
            raise ValueError(f"Customer {customer_id} not found")
        return self.customers[customer_id]
    
    def get_all_customers(self):
        """Get all customers."""
        return list(self.customers.values())
    
    # ==================== RENTAL MANAGEMENT ====================
    
    def create_rental(self, customer_id, vehicle_id, start_date, end_date):
        """
        Create a new rental.
        
        Args:
            customer_id (int): Customer ID
            vehicle_id (int): Vehicle ID
            start_date (datetime): Start date
            end_date (datetime): End date
            
        Returns:
            Rental: The created rental
            
        Raises:
            ValueError: If rental cannot be created
        """
        customer = self.get_customer(customer_id)
        vehicle = self.get_vehicle(vehicle_id)
        
        # Validation checks
        if not vehicle.is_available():
            raise ValueError(f"Vehicle {vehicle_id} is not available")
        
        if not customer.can_rent_vehicle(vehicle):
            raise ValueError(f"Customer {customer_id} cannot rent this vehicle")
        
        if start_date >= end_date:
            raise ValueError("Start date must be before end date")
        
        # Check for overlapping rentals
        for rental in self.rentals.values():
            if rental.vehicle.vehicle_id == vehicle_id and rental.status == RentalStatus.ACTIVE:
                if (start_date < rental.end_date and end_date > rental.start_date):
                    raise ValueError(f"Vehicle {vehicle_id} is already reserved for these dates")
        
        # Create rental
        rental_id = self.next_rental_id
        self.next_rental_id += 1
        
        rental = Rental(rental_id, customer, vehicle, start_date, end_date)
        self.rentals[rental_id] = rental
        
        # Update vehicle state
        vehicle.set_state(VehicleState.RENTED)
        
        return rental
    
    def complete_rental(self, rental_id, actual_return_date=None):
        """
        Complete a rental.
        
        Args:
            rental_id (int): Rental ID
            actual_return_date (datetime): Actual return date (optional)
        """
        if rental_id not in self.rentals:
            raise ValueError(f"Rental {rental_id} not found")
        
        rental = self.rentals[rental_id]
        rental.complete_rental(actual_return_date)
        
        # Update vehicle state
        rental.vehicle.set_state(VehicleState.AVAILABLE)
    
    def cancel_rental(self, rental_id):
        """Cancel a rental."""
        if rental_id not in self.rentals:
            raise ValueError(f"Rental {rental_id} not found")
        
        rental = self.rentals[rental_id]
        rental.cancel_rental()
        
        # Update vehicle state
        rental.vehicle.set_state(VehicleState.AVAILABLE)
    
    def extend_rental(self, rental_id, new_end_date):
        """Extend a rental."""
        if rental_id not in self.rentals:
            raise ValueError(f"Rental {rental_id} not found")
        
        rental = self.rentals[rental_id]
        rental.extend_rental(new_end_date)
    
    def get_rental(self, rental_id):
        """Get a rental by ID."""
        if rental_id not in self.rentals:
            raise ValueError(f"Rental {rental_id} not found")
        return self.rentals[rental_id]
    
    def get_all_rentals(self):
        """Get all rentals."""
        return list(self.rentals.values())
    
    def get_active_rentals(self):
        """Get all active rentals."""
        return [r for r in self.rentals.values() if r.status == RentalStatus.ACTIVE]
    
    def get_completed_rentals(self):
        """Get all completed rentals."""
        return [r for r in self.rentals.values() if r.status == RentalStatus.COMPLETED]
    
    def get_overdue_rentals(self):
        """Get all overdue rentals."""
        return [r for r in self.get_active_rentals() if r.is_overdue()]
    
    # ==================== SEARCH & FILTER ====================
    
    def search_vehicles(self, brand=None, category=None, max_price=None, available_only=True):
        """
        Search for vehicles with filters.
        
        Args:
            brand (str): Filter by brand
            category (str): Filter by category
            max_price (float): Maximum daily rate
            available_only (bool): Only show available vehicles
            
        Returns:
            list: Filtered list of vehicles
        """
        results = self.vehicles.values()
        
        if available_only:
            results = [v for v in results if v.is_available()]
        
        if brand:
            results = [v for v in results if v.brand.lower() == brand.lower()]
        
        if category:
            results = [v for v in results if v.category.lower() == category.lower()]
        
        if max_price:
            results = [v for v in results if v.daily_rate <= max_price]
        
        return list(results)
    
    def search_customers(self, last_name=None, min_rentals=None):
        """
        Search for customers.
        
        Args:
            last_name (str): Filter by last name
            min_rentals (int): Minimum number of rentals
            
        Returns:
            list: Filtered list of customers
        """
        results = self.customers.values()
        
        if last_name:
            results = [c for c in results if c.last_name.lower() == last_name.lower()]
        
        if min_rentals:
            results = [c for c in results if c.get_rental_count() >= min_rentals]
        
        return list(results)
    
    # ==================== REPORTS ====================
    
    def generate_fleet_report(self):
        """Generate a report on the vehicle fleet."""
        total_vehicles = len(self.vehicles)
        available = len(self.get_available_vehicles())
        in_maintenance = sum(1 for v in self.vehicles.values() if v.state == VehicleState.MAINTENANCE)
        rented = sum(1 for v in self.vehicles.values() if v.state == VehicleState.RENTED)
        
        report = {
            'total_vehicles': total_vehicles,
            'available': available,
            'rented': rented,
            'in_maintenance': in_maintenance,
            'reserved': total_vehicles - available - rented - in_maintenance,
            'vehicles_by_type': {
                'cars': len([v for v in self.vehicles.values() if isinstance(v, Car)]),
                'trucks': len([v for v in self.vehicles.values() if isinstance(v, Truck)]),
                'motorcycles': len([v for v in self.vehicles.values() if isinstance(v, Motorcycle)])
            }
        }
        return report
    
    def generate_active_rentals_report(self):
        """Generate a report on active rentals."""
        active = self.get_active_rentals()
        overdue = self.get_overdue_rentals()
        
        report = {
            'total_active_rentals': len(active),
            'overdue_rentals': len(overdue),
            'overdue_details': [(r.rental_id, r.customer.get_full_name(), r.vehicle.vehicle_id) for r in overdue],
            'total_expected_revenue': sum(r.total_cost for r in active)
        }
        return report
    
    def generate_revenue_report(self):
        """Generate a revenue report."""
        completed = self.get_completed_rentals()
        
        if not completed:
            return {
                'total_revenue': 0.0,
                'total_rentals': 0,
                'average_rental_value': 0.0,
                'total_penalties': 0.0
            }
        
        total_revenue = sum(r.total_cost for r in completed)
        total_penalties = sum(r.late_return_penalty for r in completed)
        average_value = total_revenue / len(completed)
        
        report = {
            'total_revenue': total_revenue,
            'total_rentals': len(completed),
            'average_rental_value': average_value,
            'total_penalties': total_penalties,
            'base_revenue': total_revenue - total_penalties
        }
        return report
    
    def generate_customer_statistics(self):
        """Generate customer statistics."""
        if not self.customers:
            return {
                'total_customers': 0,
                'total_rentals': 0,
                'average_rentals_per_customer': 0.0,
                'total_revenue_from_customers': 0.0
            }
        
        total_customers = len(self.customers)
        total_rentals = sum(c.get_rental_count() for c in self.customers.values())
        total_spent = sum(c.total_spent for c in self.customers.values())
        
        report = {
            'total_customers': total_customers,
            'total_rentals': total_rentals,
            'average_rentals_per_customer': total_rentals / total_customers if total_customers > 0 else 0,
            'total_revenue_from_customers': total_spent,
            'average_spent_per_customer': total_spent / total_customers if total_customers > 0 else 0
        }
        return report
    
    def print_fleet_status(self):
        """Print a nicely formatted fleet status."""
        print("\n" + "="*70)
        print("FLEET STATUS REPORT")
        print("="*70)
        
        for vehicle in sorted(self.vehicles.values(), key=lambda v: v.vehicle_id):
            print(f"  {vehicle}")
        
        print("\n" + "-"*70)
        report = self.generate_fleet_report()
        print(f"Total Vehicles: {report['total_vehicles']} | Available: {report['available']} | "
              f"Rented: {report['rented']} | Maintenance: {report['in_maintenance']}")
        print("="*70 + "\n")
    
    def print_active_rentals(self):
        """Print all active rentals."""
        print("\n" + "="*70)
        print("ACTIVE RENTALS REPORT")
        print("="*70)
        
        active = self.get_active_rentals()
        if not active:
            print("  No active rentals")
        else:
            for rental in sorted(active, key=lambda r: r.rental_id):
                overdue = " [OVERDUE]" if rental.is_overdue() else ""
                print(f"  {rental}{overdue}")
        
        print("="*70 + "\n")
    
    def print_revenue_report(self):
        """Print revenue report."""
        print("\n" + "="*70)
        print("REVENUE REPORT")
        print("="*70)
        
        report = self.generate_revenue_report()
        print(f"  Total Revenue: ${report['total_revenue']:.2f}")
        print(f"  Total Rentals: {report['total_rentals']}")
        print(f"  Average Rental Value: ${report['average_rental_value']:.2f}")
        print(f"  Total Penalties: ${report['total_penalties']:.2f}")
        print(f"  Base Revenue (excluding penalties): ${report['base_revenue']:.2f}")
        print("="*70 + "\n")
    
    def __str__(self):
        """String representation."""
        return (f"CarRentalSystem - Vehicles: {len(self.vehicles)}, "
                f"Customers: {len(self.customers)}, Rentals: {len(self.rentals)}")