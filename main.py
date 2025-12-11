"""
Test and demonstration file for the Car Rental System.
Shows practical usage of all classes and features.
"""

from datetime import datetime, timedelta
from CarRentalSystem import CarRentalSystem
from Customer import LicenseType


def main():
    """Main demonstration of the car rental system."""
    
    # Initialize the system
    system = CarRentalSystem()
    print("Car Rental Management System - Demo")
    print("="*70)
    
    # ==================== ADD VEHICLES ====================
    print("\n1. Adding vehicles to the fleet...")
    print("-"*70)
    
    # Add cars
    car1 = system.add_vehicle("Toyota", "Corolla", "sedan", 50.0, num_doors=4, fuel_type="petrol")
    print(f"✓ Added: {car1}")
    
    car2 = system.add_vehicle("BMW", "X5", "SUV", 120.0, num_doors=4, fuel_type="diesel")
    print(f"✓ Added: {car2}")
    
    car3 = system.add_vehicle("Hyundai", "i10", "hatchback", 35.0, num_doors=5, fuel_type="petrol")
    print(f"✓ Added: {car3}")
    
    # Add trucks
    truck1 = system.add_vehicle("Volvo", "FH16", "truck", 200.0, payload_capacity=25.0)
    print(f"✓ Added: {truck1}")
    
    # Add motorcycles
    moto1 = system.add_vehicle("Harley-Davidson", "Street 750", "cruiser", 60.0, engine_cc=750)
    print(f"✓ Added: {moto1}")
    
    moto2 = system.add_vehicle("Yamaha", "YZF-R1", "sport", 80.0, engine_cc=1000)
    print(f"✓ Added: {moto2}")
    
    print(f"\nTotal vehicles added: {len(system.get_all_vehicles())}")
    
    # ==================== ADD CUSTOMERS ====================
    print("\n2. Registering customers...")
    print("-"*70)
    
    cust1 = system.add_customer("John", "Doe", 25, LicenseType.AUTO_LIGHT)
    print(f"✓ Registered: {cust1}")
    
    cust2 = system.add_customer("Alice", "Smith", 35, LicenseType.AUTO_HEAVY)
    print(f"✓ Registered: {cust2}")
    
    cust3 = system.add_customer("Bob", "Johnson", 22, LicenseType.MOTORCYCLE)
    print(f"✓ Registered: {cust3}")
    
    cust4 = system.add_customer("Emma", "Williams", 28, LicenseType.AUTO_LIGHT)
    print(f"✓ Registered: {cust4}")
    
    print(f"\nTotal customers: {len(system.get_all_customers())}")
    
    # ==================== CREATE RENTALS ====================
    print("\n3. Creating rental reservations...")
    print("-"*70)
    
    # Rental 1: John renting a Toyota Corolla for 3 days
    start1 = datetime.now()
    end1 = start1 + timedelta(days=3)
    rental1 = system.create_rental(cust1.customer_id, car1.vehicle_id, start1, end1)
    print(f"✓ Rental created: {rental1}")
    print(f"  Cost: ${rental1.total_cost:.2f}")
    
    # Rental 2: Alice renting a Volvo truck for 5 days
    start2 = datetime.now()
    end2 = start2 + timedelta(days=5)
    rental2 = system.create_rental(cust2.customer_id, truck1.vehicle_id, start2, end2)
    print(f"✓ Rental created: {rental2}")
    print(f"  Cost: ${rental2.total_cost:.2f}")
    
    # Rental 3: Bob renting a Harley motorcycle for 2 days
    start3 = datetime.now()
    end3 = start3 + timedelta(days=2)
    rental3 = system.create_rental(cust3.customer_id, moto1.vehicle_id, start3, end3)
    print(f"✓ Rental created: {rental3}")
    print(f"  Cost: ${rental3.total_cost:.2f}")
    
    # Rental 4: Emma renting a BMW X5 for 7 days
    start4 = datetime.now()
    end4 = start4 + timedelta(days=7)
    rental4 = system.create_rental(cust4.customer_id, car2.vehicle_id, start4, end4)
    print(f"✓ Rental created: {rental4}")
    print(f"  Cost: ${rental4.total_cost:.2f}")
    
    # ==================== PRINT FLEET STATUS ====================
    print("\n4. Fleet Status After Rentals")
    system.print_fleet_status()
    
    # ==================== PRINT ACTIVE RENTALS ====================
    print("5. Active Rentals Report")
    system.print_active_rentals()
    
    # ==================== COMPLETE SOME RENTALS ====================
    print("6. Completing rentals...")
    print("-"*70)
    
    # Complete rental 1 (on time)
    system.complete_rental(rental1.rental_id)
    print(f"✓ Rental {rental1.rental_id} completed on time - Final cost: ${rental1.total_cost:.2f}")
    
    # Complete rental 3 (2 days late - 2 * $60 * 0.5 = $60 penalty)
    late_return = rental3.end_date + timedelta(days=2)
    system.complete_rental(rental3.rental_id, late_return)
    print(f"✓ Rental {rental3.rental_id} completed 2 days late")
    print(f"  Penalty: ${rental3.late_return_penalty:.2f}")
    print(f"  Final cost: ${rental3.total_cost:.2f}")
    
    # ==================== VEHICLE MAINTENANCE ====================
    print("\n7. Vehicle Maintenance")
    print("-"*70)
    
    # Complete rental 2 first to free up the truck
    system.complete_rental(rental2.rental_id)
    print(f"✓ Rental {rental2.rental_id} completed")
    
    # Schedule maintenance for the truck
    system.schedule_vehicle_maintenance(truck1.vehicle_id, "Engine oil change and inspection", 2)
    print(f"✓ Maintenance scheduled for vehicle {truck1.vehicle_id}")
    print(f"  Vehicle state: {truck1.state.value}")
    
    # Complete maintenance
    system.complete_vehicle_maintenance(truck1.vehicle_id)
    print(f"✓ Maintenance completed for vehicle {truck1.vehicle_id}")
    print(f"  Vehicle state: {truck1.state.value}")
    
    # ==================== SEARCH FUNCTIONALITY ====================
    print("\n8. Search Functionality")
    print("-"*70)
    
    # Search for available sedans
    sedans = system.search_vehicles(category='sedan', available_only=True)
    print(f"Available sedans: {len(sedans)}")
    for car in sedans:
        print(f"  - {car}")
    
    # Search for vehicles under $100/day
    budget_vehicles = system.search_vehicles(max_price=100.0, available_only=True)
    print(f"\nVehicles under $100/day: {len(budget_vehicles)}")
    for vehicle in budget_vehicles:
        print(f"  - {vehicle.brand} {vehicle.model}: ${vehicle.daily_rate}/day")
    
    # ==================== CUSTOMER HISTORY ====================
    print("\n9. Customer Rental History")
    print("-"*70)
    
    for customer in system.get_all_customers():
        print(f"\n{customer.get_full_name()}:")
        print(f"  Total rentals: {customer.get_rental_count()}")
        print(f"  Total spent: ${customer.total_spent:.2f}")
        print(f"  Discount rate: {customer.get_discount_rate()*100:.1f}%")
        
        if customer.get_rental_count() > 0:
            print(f"  Rentals:")
            for rental in customer.get_rental_history():
                print(f"    - Rental {rental.rental_id}: {rental.vehicle.brand} {rental.vehicle.model} - ${rental.total_cost:.2f}")
    
    # ==================== FINANCIAL REPORTS ====================
    print("\n10. Financial Reports")
    system.print_revenue_report()
    
    # Customer statistics
    print("11. Customer Statistics")
    print("="*70)
    stats = system.generate_customer_statistics()
    print(f"Total customers: {stats['total_customers']}")
    print(f"Total rentals: {stats['total_rentals']}")
    print(f"Average rentals per customer: {stats['average_rentals_per_customer']:.2f}")
    print(f"Total revenue from customers: ${stats['total_revenue_from_customers']:.2f}")
    print(f"Average spent per customer: ${stats['average_spent_per_customer']:.2f}")
    print("="*70 + "\n")
    
    # ==================== FINAL SYSTEM STATUS ====================
    print("12. Final System Status")
    print("="*70)
    fleet_report = system.generate_fleet_report()
    print(f"Total vehicles: {fleet_report['total_vehicles']}")
    print(f"Available: {fleet_report['available']}")
    print(f"Rented: {fleet_report['rented']}")
    print(f"In maintenance: {fleet_report['in_maintenance']}")
    print(f"Vehicles by type:")
    print(f"  - Cars: {fleet_report['vehicles_by_type']['cars']}")
    print(f"  - Trucks: {fleet_report['vehicles_by_type']['trucks']}")
    print(f"  - Motorcycles: {fleet_report['vehicles_by_type']['motorcycles']}")
    
    print(f"\nActive rentals: {len(system.get_active_rentals())}")
    print(f"Completed rentals: {len(system.get_completed_rentals())}")
    print(f"\n{system}")
    print("="*70)


if __name__ == "__main__":
    main()
