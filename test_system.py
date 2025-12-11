"""
Unit tests for the Car Rental Management System.
Tests all classes and functionality.
"""

import unittest
from datetime import datetime, timedelta
from CarRentalSystem import CarRentalSystem
from Vehicule import Car, Truck, Motorcycle, VehicleState
from Customer import Customer, LicenseType
from Rental import Rental, RentalStatus


class TestVehicleHierarchy(unittest.TestCase):
    """Test vehicle classes."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.car = Car(1, "Toyota", "Corolla", "sedan", 50.0, 4, "petrol")
        self.truck = Truck(2, "Volvo", "FH16", "truck", 200.0, 25.0)
        self.motorcycle = Motorcycle(3, "Harley", "Street", "cruiser", 60.0, 750)
    
    def test_car_creation(self):
        """Test car creation."""
        self.assertEqual(self.car.vehicle_id, 1)
        self.assertEqual(self.car.brand, "Toyota")
        self.assertEqual(self.car.daily_rate, 50.0)
        self.assertTrue(self.car.is_available())
    
    def test_vehicle_eligibility(self):
        """Test age eligibility for vehicles."""
        # Car requires 18+
        self.assertTrue(self.car.is_eligible_for_customer(18))
        self.assertFalse(self.car.is_eligible_for_customer(17))
        
        # Truck requires 21+
        self.assertTrue(self.truck.is_eligible_for_customer(21))
        self.assertFalse(self.truck.is_eligible_for_customer(20))
        
        # Motorcycle requires 18+
        self.assertTrue(self.motorcycle.is_eligible_for_customer(18))
        self.assertFalse(self.motorcycle.is_eligible_for_customer(17))
    
    def test_maintenance_scheduling(self):
        """Test vehicle maintenance."""
        self.assertEqual(len(self.car.maintenance_history), 0)
        
        self.car.schedule_maintenance("Oil change", 1)
        self.assertEqual(len(self.car.maintenance_history), 1)
        self.assertEqual(self.car.state, VehicleState.MAINTENANCE)
        
        self.car.complete_maintenance()
        self.assertEqual(self.car.state, VehicleState.AVAILABLE)
        self.assertTrue(self.car.maintenance_history[0]['completed'])
    
    def test_vehicle_state_changes(self):
        """Test vehicle state transitions."""
        self.assertEqual(self.car.state, VehicleState.AVAILABLE)
        
        self.car.set_state(VehicleState.RENTED)
        self.assertEqual(self.car.state, VehicleState.RENTED)
        self.assertFalse(self.car.is_available())
        
        self.car.set_state(VehicleState.AVAILABLE)
        self.assertTrue(self.car.is_available())


class TestCustomer(unittest.TestCase):
    """Test customer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.customer = Customer(1, "John", "Doe", 25, LicenseType.AUTO_LIGHT)
    
    def test_customer_creation(self):
        """Test customer creation."""
        self.assertEqual(self.customer.customer_id, 1)
        self.assertEqual(self.customer.get_full_name(), "John Doe")
        self.assertEqual(self.customer.age, 25)
    
    def test_customer_license_types(self):
        """Test different license types."""
        car_customer = Customer(1, "John", "Doe", 25, LicenseType.AUTO_LIGHT)
        truck_customer = Customer(2, "Alice", "Smith", 35, LicenseType.AUTO_HEAVY)
        moto_customer = Customer(3, "Bob", "Johnson", 22, LicenseType.MOTORCYCLE)
        
        self.assertEqual(car_customer.license_type, LicenseType.AUTO_LIGHT)
        self.assertEqual(truck_customer.license_type, LicenseType.AUTO_HEAVY)
        self.assertEqual(moto_customer.license_type, LicenseType.MOTORCYCLE)
    
    def test_discount_calculation(self):
        """Test loyalty discount calculation."""
        # No rentals = no discount
        self.assertEqual(self.customer.get_discount_rate(), 0.0)
        
        # Mock rental history
        self.customer.rental_history = list(range(5))
        self.assertEqual(self.customer.get_discount_rate(), 0.05)  # 5% at 5 rentals
        
        self.customer.rental_history = list(range(10))
        self.assertEqual(self.customer.get_discount_rate(), 0.10)  # 10% at 10 rentals
        
        self.customer.rental_history = list(range(20))
        self.assertEqual(self.customer.get_discount_rate(), 0.15)  # 15% at 20 rentals


class TestRental(unittest.TestCase):
    """Test rental class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.car = Car(1, "Toyota", "Corolla", "sedan", 100.0, 4, "petrol")
        self.customer = Customer(1, "John", "Doe", 25, LicenseType.AUTO_LIGHT)
        
        self.start = datetime(2025, 1, 1, 10, 0, 0)
        self.end = datetime(2025, 1, 4, 10, 0, 0)  # 3 days
        
        self.rental = Rental(1, self.customer, self.car, self.start, self.end)
    
    def test_rental_creation(self):
        """Test rental creation."""
        self.assertEqual(self.rental.rental_id, 1)
        self.assertEqual(self.rental.customer, self.customer)
        self.assertEqual(self.rental.vehicle, self.car)
        self.assertEqual(self.rental.status, RentalStatus.ACTIVE)
    
    def test_rental_cost_calculation(self):
        """Test rental cost calculation."""
        # 3 days at $100/day = $300
        expected_cost = 100.0 * 3
        self.assertEqual(self.rental.total_cost, expected_cost)
    
    def test_rental_with_discount(self):
        """Test rental cost with customer discount."""
        # Create customer with some rentals for discount
        customer = Customer(2, "Alice", "Smith", 30, LicenseType.AUTO_LIGHT)
        customer.rental_history = list(range(5))  # 5 rentals = 5% discount
        
        rental = Rental(2, customer, self.car, self.start, self.end)
        # 3 days at $100/day = $300, with 5% discount = $285
        expected_cost = 300.0 * 0.95
        self.assertEqual(rental.total_cost, expected_cost)
    
    def test_invalid_rental_dates(self):
        """Test invalid rental dates."""
        with self.assertRaises(ValueError):
            Rental(3, self.customer, self.car, self.end, self.start)  # end before start
    
    def test_late_return_penalty(self):
        """Test late return penalty calculation."""
        self.rental.complete_rental(self.end + timedelta(days=2))
        
        # 2 days late * $100/day * 0.5 = $100 penalty
        expected_penalty = 100.0 * 2 * 0.5
        self.assertEqual(self.rental.late_return_penalty, expected_penalty)
    
    def test_rental_cancellation(self):
        """Test rental cancellation."""
        self.rental.cancel_rental()
        self.assertEqual(self.rental.status, RentalStatus.CANCELLED)
        self.assertEqual(self.rental.total_cost, 0)


class TestCarRentalSystem(unittest.TestCase):
    """Test main system class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.system = CarRentalSystem()
        
        # Add vehicles
        self.car = self.system.add_vehicle("Toyota", "Corolla", "sedan", 50.0, 
                                          num_doors=4, fuel_type="petrol")
        self.truck = self.system.add_vehicle("Volvo", "FH16", "truck", 200.0, 
                                            payload_capacity=25.0)
        
        # Add customers
        self.customer1 = self.system.add_customer("John", "Doe", 25, LicenseType.AUTO_LIGHT)
        self.customer2 = self.system.add_customer("Alice", "Smith", 35, LicenseType.AUTO_HEAVY)
    
    def test_add_vehicles(self):
        """Test vehicle addition."""
        self.assertEqual(len(self.system.get_all_vehicles()), 2)
        self.assertEqual(self.car.vehicle_id, 1)
        self.assertEqual(self.truck.vehicle_id, 2)
    
    def test_add_customers(self):
        """Test customer addition."""
        self.assertEqual(len(self.system.get_all_customers()), 2)
        self.assertEqual(self.customer1.customer_id, 1)
    
    def test_create_rental(self):
        """Test rental creation."""
        start = datetime.now()
        end = start + timedelta(days=3)
        
        rental = self.system.create_rental(self.customer1.customer_id, 
                                          self.car.vehicle_id, start, end)
        
        self.assertIsNotNone(rental)
        self.assertEqual(rental.status, RentalStatus.ACTIVE)
        self.assertEqual(self.car.state, VehicleState.RENTED)
    
    def test_cannot_rent_unavailable_vehicle(self):
        """Test rental fails for unavailable vehicle."""
        start = datetime.now()
        end = start + timedelta(days=3)
        
        # First rental uses the car
        self.system.create_rental(self.customer1.customer_id, self.car.vehicle_id, start, end)
        
        # Second rental should fail
        with self.assertRaises(ValueError):
            self.system.create_rental(self.customer2.customer_id, self.car.vehicle_id, start, end)
    
    def test_customer_eligibility(self):
        """Test customer eligibility checks."""
        start = datetime.now()
        end = start + timedelta(days=3)
        
        # Customer with AUTO_LIGHT license can rent car
        rental = self.system.create_rental(self.customer1.customer_id, 
                                          self.car.vehicle_id, start, end)
        self.assertIsNotNone(rental)
    
    def test_complete_rental(self):
        """Test rental completion."""
        start = datetime.now()
        end = start + timedelta(days=3)
        
        rental = self.system.create_rental(self.customer1.customer_id, 
                                          self.car.vehicle_id, start, end)
        rental_id = rental.rental_id
        
        self.system.complete_rental(rental_id)
        
        completed_rental = self.system.get_rental(rental_id)
        self.assertEqual(completed_rental.status, RentalStatus.COMPLETED)
        self.assertEqual(self.car.state, VehicleState.AVAILABLE)
    
    def test_search_vehicles_by_category(self):
        """Test vehicle search by category."""
        results = self.system.search_vehicles(category="sedan", available_only=True)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].brand, "Toyota")
    
    def test_search_vehicles_by_price(self):
        """Test vehicle search by price."""
        results = self.system.search_vehicles(max_price=100.0, available_only=True)
        self.assertEqual(len(results), 1)  # Only the $50 car
    
    def test_available_vehicles_count(self):
        """Test available vehicles tracking."""
        start = datetime.now()
        end = start + timedelta(days=3)
        
        self.assertEqual(len(self.system.get_available_vehicles()), 2)
        
        # Create rental
        self.system.create_rental(self.customer1.customer_id, 
                                 self.car.vehicle_id, start, end)
        
        self.assertEqual(len(self.system.get_available_vehicles()), 1)
        
        # Complete rental
        self.system.complete_rental(1)
        
        self.assertEqual(len(self.system.get_available_vehicles()), 2)
    
    def test_fleet_report(self):
        """Test fleet report generation."""
        start = datetime.now()
        end = start + timedelta(days=3)
        
        # Create some rentals
        self.system.create_rental(self.customer1.customer_id, self.car.vehicle_id, start, end)
        self.system.create_rental(self.customer2.customer_id, self.truck.vehicle_id, start, end)
        
        report = self.system.generate_fleet_report()
        
        self.assertEqual(report['total_vehicles'], 2)
        self.assertEqual(report['available'], 0)
        self.assertEqual(report['rented'], 2)
    
    def test_revenue_report(self):
        """Test revenue report generation."""
        start = datetime.now()
        end = start + timedelta(days=3)
        
        # Create and complete a rental
        rental = self.system.create_rental(self.customer1.customer_id, 
                                          self.car.vehicle_id, start, end)
        self.system.complete_rental(rental.rental_id)
        
        report = self.system.generate_revenue_report()
        
        self.assertEqual(report['total_rentals'], 1)
        self.assertGreater(report['total_revenue'], 0)
    
    def test_customer_statistics(self):
        """Test customer statistics."""
        start = datetime.now()
        end = start + timedelta(days=3)
        
        # Create rentals
        rental1 = self.system.create_rental(self.customer1.customer_id, 
                                           self.car.vehicle_id, start, end)
        self.system.complete_rental(rental1.rental_id)
        
        stats = self.system.generate_customer_statistics()
        
        self.assertEqual(stats['total_customers'], 2)
        self.assertEqual(stats['total_rentals'], 1)


class TestAdvancedScenarios(unittest.TestCase):
    """Test advanced scenarios and edge cases."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.system = CarRentalSystem()
        self.car = self.system.add_vehicle("Toyota", "Corolla", "sedan", 100.0, 
                                          num_doors=4, fuel_type="petrol")
        self.customer = self.system.add_customer("John", "Doe", 25, LicenseType.AUTO_LIGHT)
    
    def test_extend_rental(self):
        """Test rental extension."""
        start = datetime.now()
        end = start + timedelta(days=3)
        
        rental = self.system.create_rental(self.customer.customer_id, 
                                          self.car.vehicle_id, start, end)
        original_cost = rental.total_cost
        
        # Extend by 2 more days
        new_end = end + timedelta(days=2)
        self.system.extend_rental(rental.rental_id, new_end)
        
        # Cost should increase
        self.assertGreater(rental.total_cost, original_cost)
    
    def test_overlapping_rentals_prevention(self):
        """Test prevention of overlapping rentals."""
        customer2 = self.system.add_customer("Alice", "Smith", 30, LicenseType.AUTO_LIGHT)
        
        start1 = datetime.now()
        end1 = start1 + timedelta(days=3)
        
        # First rental
        self.system.create_rental(self.customer.customer_id, self.car.vehicle_id, start1, end1)
        
        # Overlapping rental should fail
        start2 = start1 + timedelta(days=2)
        end2 = start2 + timedelta(days=2)
        
        with self.assertRaises(ValueError):
            self.system.create_rental(customer2.customer_id, self.car.vehicle_id, start2, end2)
    
    def test_vehicle_maintenance_blocks_rental(self):
        """Test that maintenance prevents rentals."""
        start = datetime.now()
        end = start + timedelta(days=3)
        
        # Schedule maintenance
        self.system.schedule_vehicle_maintenance(self.car.vehicle_id, "Oil change", 1)
        
        # Rental should fail
        with self.assertRaises(ValueError):
            self.system.create_rental(self.customer.customer_id, self.car.vehicle_id, start, end)


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == "__main__":
    run_tests()
