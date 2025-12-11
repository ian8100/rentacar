"""
Practical Usage Examples - Car Rental Management System
Demonstrates real-world scenarios and best practices.
"""

from CarRentalSystem import CarRentalSystem
from Customer import LicenseType
from datetime import datetime, timedelta


def example_1_basic_rental():
    """Example 1: Simple rental operation."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Rental Operation")
    print("="*70)
    
    system = CarRentalSystem()
    
    # Add a vehicle
    vehicle = system.add_vehicle("Honda", "Civic", "sedan", 45.0, 
                                num_doors=4, fuel_type="petrol")
    print(f"Added vehicle: {vehicle}")
    
    # Register a customer
    customer = system.add_customer("Sarah", "Johnson", 28, LicenseType.AUTO_LIGHT)
    print(f"Registered customer: {customer}")
    
    # Create a rental (3 days starting today)
    start_date = datetime.now()
    end_date = start_date + timedelta(days=3)
    
    try:
        rental = system.create_rental(customer.customer_id, vehicle.vehicle_id, 
                                     start_date, end_date)
        print(f"✓ Rental created: {rental}")
        print(f"  Duration: {rental.get_rental_duration_days()} days")
        print(f"  Cost: ${rental.total_cost:.2f}")
    except ValueError as e:
        print(f"✗ Rental failed: {e}")
    
    # Complete the rental
    system.complete_rental(rental.rental_id)
    print(f"✓ Rental completed")
    print(f"  Final cost: ${rental.total_cost:.2f}")
    print(f"  Vehicle available again: {vehicle.is_available()}")


def example_2_late_return_penalty():
    """Example 2: Handle late returns with penalties."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Late Return with Penalties")
    print("="*70)
    
    system = CarRentalSystem()
    
    # Setup
    truck = system.add_vehicle("Mercedes", "Sprinter", "truck", 150.0, 
                              payload_capacity=3.5)
    customer = system.add_customer("Mike", "Brown", 32, LicenseType.AUTO_HEAVY)
    
    # 5-day rental
    start = datetime.now()
    end = start + timedelta(days=5)
    
    rental = system.create_rental(customer.customer_id, truck.vehicle_id, start, end)
    print(f"Initial rental: {rental.get_rental_duration_days()} days @ ${truck.daily_rate}/day")
    print(f"Base cost: ${rental.total_cost:.2f}")
    
    # Return 3 days late
    actual_return = end + timedelta(days=3)
    print(f"\nVehicle returned 3 days late")
    print(f"Late days: {(actual_return - end).days}")
    
    system.complete_rental(rental.rental_id, actual_return)
    
    print(f"\n✓ Rental completed:")
    print(f"  Original cost: ${rental.total_cost - rental.late_return_penalty:.2f}")
    print(f"  Late penalty: ${rental.late_return_penalty:.2f}")
    print(f"    ({(actual_return - end).days} days × ${truck.daily_rate} × 0.5)")
    print(f"  Total cost: ${rental.total_cost:.2f}")
    print(f"  Penalty increase: {(rental.late_return_penalty / (rental.total_cost - rental.late_return_penalty) * 100):.1f}%")


def example_3_loyalty_discount():
    """Example 3: Loyalty discount for frequent customers."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Loyalty Discount System")
    print("="*70)
    
    system = CarRentalSystem()
    
    # Setup
    car = system.add_vehicle("Tesla", "Model 3", "sedan", 80.0)
    customer = system.add_customer("Alex", "Davis", 42, LicenseType.AUTO_LIGHT)
    
    print(f"Customer: {customer.get_full_name()}")
    print(f"Initial rentals: {customer.get_rental_count()}")
    print(f"Current discount: {customer.get_discount_rate()*100:.0f}%")
    
    # Simulate 15 previous rentals
    print(f"\nSimulating 15 previous rentals...")
    customer.rental_history = list(range(15))
    
    print(f"Updated rentals: {customer.get_rental_count()}")
    print(f"New discount: {customer.get_discount_rate()*100:.0f}%")
    
    # Now create a new rental
    start = datetime.now()
    end = start + timedelta(days=3)
    rental = system.create_rental(customer.customer_id, car.vehicle_id, start, end)
    
    base_cost = car.daily_rate * 3
    discount_rate = customer.get_discount_rate()
    discount_amount = base_cost * discount_rate
    
    print(f"\nNew rental:")
    print(f"  Base cost (3 days × ${car.daily_rate}): ${base_cost:.2f}")
    print(f"  Discount ({discount_rate*100:.0f}%): -${discount_amount:.2f}")
    print(f"  Final cost: ${rental.total_cost:.2f}")
    print(f"  Saved: ${discount_amount:.2f}")


def example_4_search_and_filter():
    """Example 4: Search and filter vehicles."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Search and Filter Vehicles")
    print("="*70)
    
    system = CarRentalSystem()
    
    # Add variety of vehicles
    vehicles = [
        ("Toyota", "Corolla", "sedan", 45.0),
        ("BMW", "X5", "SUV", 120.0),
        ("Hyundai", "i20", "hatchback", 35.0),
        ("Volvo", "FH16", "truck", 250.0),
        ("Harley-Davidson", "Street 750", "cruiser", 70.0),
    ]
    
    for brand, model, category, rate in vehicles:
        system.add_vehicle(brand, model, category, rate)
    
    print(f"Total vehicles in fleet: {len(system.get_all_vehicles())}\n")
    
    # Search 1: Budget vehicles
    print("Search 1: Vehicles under $100/day")
    budget = system.search_vehicles(max_price=100.0)
    for v in budget:
        print(f"  ✓ {v.brand} {v.model}: ${v.daily_rate}/day")
    
    # Search 2: By category
    print("\nSearch 2: All sedans")
    sedans = system.search_vehicles(category="sedan")
    for v in sedans:
        print(f"  ✓ {v.brand} {v.model}: ${v.daily_rate}/day")
    
    # Search 3: By brand
    print("\nSearch 3: Toyota vehicles")
    toyota = system.search_vehicles(brand="Toyota")
    for v in toyota:
        print(f"  ✓ {v.brand} {v.model} ({v.category}): ${v.daily_rate}/day")
    
    # Search 4: Expensive vehicles
    print("\nSearch 4: Premium vehicles (>$100/day)")
    premium = system.search_vehicles(max_price=300.0, available_only=False)
    premium = [v for v in premium if v.daily_rate > 100]
    for v in premium:
        print(f"  ✓ {v.brand} {v.model}: ${v.daily_rate}/day")


def example_5_vehicle_maintenance():
    """Example 5: Vehicle maintenance operations."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Vehicle Maintenance")
    print("="*70)
    
    system = CarRentalSystem()
    
    vehicle = system.add_vehicle("Ford", "F-150", "truck", 180.0, payload_capacity=3.5)
    print(f"Vehicle: {vehicle}")
    print(f"State: {vehicle.state.value}")
    
    # Schedule maintenance
    print("\nScheduling maintenance: 'Engine inspection and oil change'")
    system.schedule_vehicle_maintenance(vehicle.vehicle_id, 
                                       "Engine inspection and oil change", 2)
    
    print(f"State after scheduling: {vehicle.state.value}")
    print(f"Maintenance history: {len(vehicle.maintenance_history)} record(s)")
    
    # Try to rent while in maintenance
    print("\nAttempting to rent while in maintenance...")
    customer = system.add_customer("Tom", "Wilson", 30)
    try:
        system.create_rental(customer.customer_id, vehicle.vehicle_id,
                           datetime.now(), datetime.now() + timedelta(days=1))
        print("✗ Rental should have failed!")
    except ValueError as e:
        print(f"✓ Correctly prevented: {e}")
    
    # Complete maintenance
    print("\nCompleting maintenance...")
    system.complete_vehicle_maintenance(vehicle.vehicle_id)
    print(f"State after completion: {vehicle.state.value}")
    
    # Now rental should work
    print("Attempting rental again...")
    rental = system.create_rental(customer.customer_id, vehicle.vehicle_id,
                                 datetime.now(), datetime.now() + timedelta(days=1))
    print(f"✓ Rental created: {rental}")


def example_6_customer_eligibility():
    """Example 6: Customer eligibility rules."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Customer Eligibility Rules")
    print("="*70)
    
    system = CarRentalSystem()
    
    # Add vehicles
    car = system.add_vehicle("Toyota", "Corolla", "sedan", 50.0)
    truck = system.add_vehicle("Volvo", "FH16", "truck", 200.0)
    motorcycle = system.add_vehicle("Yamaha", "YZF-R1", "sport", 80.0)
    
    # Add customers with different licenses
    car_driver = system.add_customer("John", "Smith", 25, LicenseType.AUTO_LIGHT)
    truck_driver = system.add_customer("Alice", "Jones", 35, LicenseType.AUTO_HEAVY)
    biker = system.add_customer("Bob", "Garcia", 22, LicenseType.MOTORCYCLE)
    
    start = datetime.now()
    end = start + timedelta(days=2)
    
    # Test eligibility
    tests = [
        (car_driver, car, "Can car driver rent a car?"),
        (car_driver, truck, "Can car driver rent a truck?"),
        (truck_driver, car, "Can truck driver rent a car?"),
        (truck_driver, truck, "Can truck driver rent a truck?"),
        (biker, motorcycle, "Can biker rent a motorcycle?"),
        (biker, car, "Can biker rent a car?"),
    ]
    
    for customer, vehicle, question in tests:
        can_rent = customer.can_rent_vehicle(vehicle)
        status = "✓" if can_rent else "✗"
        print(f"{status} {question} {can_rent}")
        
        if can_rent:
            try:
                rental = system.create_rental(customer.customer_id, vehicle.vehicle_id, start, end)
                system.complete_rental(rental.rental_id)
            except ValueError:
                pass  # Vehicle already rented


def example_7_reporting():
    """Example 7: Generate various reports."""
    print("\n" + "="*70)
    print("EXAMPLE 7: Comprehensive Reporting")
    print("="*70)
    
    system = CarRentalSystem()
    
    # Setup fleet and customers
    vehicles = [
        system.add_vehicle("Honda", "Civic", "sedan", 50.0),
        system.add_vehicle("BMW", "X5", "SUV", 120.0),
        system.add_vehicle("Ford", "F-150", "truck", 180.0),
    ]
    
    customers = [
        system.add_customer("John", "Doe", 25),
        system.add_customer("Jane", "Smith", 30),
        system.add_customer("Bob", "Johnson", 35),
    ]
    
    # Create some rentals
    start = datetime.now()
    for i, (customer, vehicle) in enumerate(zip(customers, vehicles)):
        end = start + timedelta(days=i+1)
        rental = system.create_rental(customer.customer_id, vehicle.vehicle_id, start, end)
        if i % 2 == 0:
            system.complete_rental(rental.rental_id)
    
    # Generate reports
    print("\n1. FLEET REPORT")
    fleet = system.generate_fleet_report()
    print(f"   Total vehicles: {fleet['total_vehicles']}")
    print(f"   Available: {fleet['available']}")
    print(f"   Rented: {fleet['rented']}")
    print(f"   Vehicle types: Cars={fleet['vehicles_by_type']['cars']}, "
          f"Trucks={fleet['vehicles_by_type']['trucks']}")
    
    print("\n2. ACTIVE RENTALS REPORT")
    active = system.generate_active_rentals_report()
    print(f"   Active rentals: {active['total_active_rentals']}")
    print(f"   Overdue rentals: {active['overdue_rentals']}")
    print(f"   Expected revenue: ${active['total_expected_revenue']:.2f}")
    
    print("\n3. REVENUE REPORT")
    revenue = system.generate_revenue_report()
    print(f"   Total revenue: ${revenue['total_revenue']:.2f}")
    print(f"   Completed rentals: {revenue['total_rentals']}")
    print(f"   Average rental value: ${revenue['average_rental_value']:.2f}")
    print(f"   Total penalties: ${revenue['total_penalties']:.2f}")
    
    print("\n4. CUSTOMER STATISTICS")
    stats = system.generate_customer_statistics()
    print(f"   Total customers: {stats['total_customers']}")
    print(f"   Total rentals: {stats['total_rentals']}")
    print(f"   Average per customer: {stats['average_rentals_per_customer']:.1f}")
    print(f"   Total revenue: ${stats['total_revenue_from_customers']:.2f}")
    print(f"   Average per customer: ${stats['average_spent_per_customer']:.2f}")


def example_8_rental_extension():
    """Example 8: Extend a rental."""
    print("\n" + "="*70)
    print("EXAMPLE 8: Extending a Rental")
    print("="*70)
    
    system = CarRentalSystem()
    
    vehicle = system.add_vehicle("Honda", "Accord", "sedan", 60.0)
    customer = system.add_customer("Emma", "Wilson", 28)
    
    start = datetime.now()
    end = start + timedelta(days=3)
    
    rental = system.create_rental(customer.customer_id, vehicle.vehicle_id, start, end)
    print(f"Original rental: {rental.get_rental_duration_days()} days")
    print(f"Original cost: ${rental.total_cost:.2f}")
    
    # Extend by 2 more days
    new_end = end + timedelta(days=2)
    print(f"\nExtending by 2 days...")
    system.extend_rental(rental.rental_id, new_end)
    
    print(f"Updated rental: {rental.get_rental_duration_days()} days")
    print(f"Updated cost: ${rental.total_cost:.2f}")
    print(f"Additional cost: ${rental.total_cost - (60 * 3):.2f}")


def main():
    """Run all examples."""
    print("\n")
    print("=" * 70)
    print("Car Rental System - Practical Usage Examples".center(70))
    print("=" * 70)
    
    examples = [
        ("Basic Rental", example_1_basic_rental),
        ("Late Return Penalty", example_2_late_return_penalty),
        ("Loyalty Discount", example_3_loyalty_discount),
        ("Search & Filter", example_4_search_and_filter),
        ("Vehicle Maintenance", example_5_vehicle_maintenance),
        ("Customer Eligibility", example_6_customer_eligibility),
        ("Comprehensive Reporting", example_7_reporting),
        ("Rental Extension", example_8_rental_extension),
    ]
    
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\nRunning all examples...\n")
    
    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n✗ Error in {name}: {e}")
    
    print("\n" + "="*70)
    print("All examples completed successfully!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
