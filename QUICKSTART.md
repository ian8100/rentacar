# Quick Start Guide - Car Rental Management System

## Overview

This is a complete object-oriented Python application for managing a car rental business. The system handles:
- Vehicle fleet management (cars, trucks, motorcycles)
- Customer registration and eligibility
- Rental creation and tracking
- Cost calculations with discounts and penalties
- Financial and operational reports

## Project Files

| File | Purpose |
|------|---------|
| `Vehicule.py` | Vehicle class hierarchy (abstract + 3 concrete types) |
| `Customer.py` | Customer management with licensing |
| `Rental.py` | Rental transaction management |
| `CarRentalSystem.py` | Central system orchestrator |
| `main.py` | Demonstration script with examples |
| `test_system.py` | 28 unit tests (all passing) |
| `README.md` | Complete documentation |

## Quick Start

### 1. Run the Demo
```bash
python main.py
```

Shows:
- Adding 6 vehicles to the fleet
- Registering 4 customers
- Creating 4 rental reservations
- Completing rentals with penalties
- Vehicle maintenance workflows
- Search and filtering
- Financial reports and statistics

**Output**: 12 comprehensive demo sections with formatted reports

### 2. Run the Tests
```bash
python -m unittest test_system -v
```

Runs 28 unit tests covering:
- Vehicle creation and state management
- Customer eligibility and discounts
- Rental calculations and penalties
- System operations (add, search, report)
- Advanced scenarios (extensions, overlaps, maintenance)

**Result**: All tests pass ✓

### 3. Use in Your Code

```python
from CarRentalSystem import CarRentalSystem
from Customer import LicenseType
from datetime import datetime, timedelta

# Create system
system = CarRentalSystem()

# Add vehicles
car = system.add_vehicle("Toyota", "Corolla", "sedan", 50.0, 
                         num_doors=4, fuel_type="petrol")

# Register customer
customer = system.add_customer("John", "Doe", 25, LicenseType.AUTO_LIGHT)

# Create rental
start = datetime.now()
end = start + timedelta(days=3)
rental = system.create_rental(customer.customer_id, car.vehicle_id, start, end)

print(f"Rental cost: ${rental.total_cost:.2f}")

# Complete rental
system.complete_rental(rental.rental_id)

# Get reports
system.print_fleet_status()
system.print_active_rentals()
system.print_revenue_report()
```

## Key Features

### Vehicle Management
- **Hierarchy**: Vehicle (abstract) → Car, Truck, Motorcycle
- **States**: Available, Rented, Maintenance, Reserved
- **Age Requirements**: Cars (18+), Trucks (21+), Motorcycles (18+)
- **Maintenance Tracking**: Schedule and complete maintenance

### Customer Management
- **License Types**: AUTO_LIGHT (cars), AUTO_HEAVY (trucks), MOTORCYCLE
- **Eligibility Checking**: Age and license validation
- **Loyalty Discounts**: 5% (5 rentals), 10% (10 rentals), 15% (20+ rentals)
- **Rental History**: Track all customer rentals

### Rental Operations
- **Cost Calculation**: Daily rate × duration - discount + penalties
- **Late Penalties**: 50% surcharge per day
- **Duration**: Minimum 1 day
- **Extension**: Extend rental to new date
- **Cancellation**: Cancel before completion

### Reporting
- **Fleet Report**: Vehicle counts by state and type
- **Active Rentals**: Current rentals and overdue status
- **Revenue Report**: Total revenue, penalties, averages
- **Customer Stats**: Total customers, rentals, spending

## Business Rules

### Age & License Requirements
```
Car (sedan, SUV, hatchback):
  - Minimum age: 18
  - License: AUTO_LIGHT or AUTO_HEAVY

Truck:
  - Minimum age: 21
  - License: AUTO_HEAVY (required)

Motorcycle (sport, cruiser, touring):
  - Minimum age: 18
  - License: MOTORCYCLE (required)
```

### Cost Calculation
```
Base Cost = Daily Rate × Duration
Discounted Cost = Base Cost × (1 - Customer Discount Rate)
Penalties = Daily Rate × 0.5 × Late Days
Final Cost = Discounted Cost + Penalties
```

### Availability
- Cannot rent unavailable vehicles
- Cannot book overlapping dates
- Cannot rent without proper license
- Cannot schedule maintenance while rented

## Example Scenarios

### Scenario 1: Simple Rental
```python
car = system.add_vehicle("Toyota", "Corolla", "sedan", 50.0)
customer = system.add_customer("John", "Doe", 25)
rental = system.create_rental(1, 1, start, end)  # 3 days = $150
system.complete_rental(1)  # On time, final cost: $150
```

### Scenario 2: Late Return with Penalty
```python
rental = system.create_rental(1, 1, start, end)  # $150 for 3 days
late_return = end + timedelta(days=2)
system.complete_rental(1, late_return)  # 2 days late
# Penalty: $50 × 0.5 × 2 = $50
# Final: $150 + $50 = $200
```

### Scenario 3: Loyal Customer with Discount
```python
customer = system.add_customer("Alice", "Smith", 30)
# ... add 10 rentals to history ...
rental = system.create_rental(2, 2, start, end)  # Auto gets 10% discount
# Cost: $150 × 0.9 = $135
```

### Scenario 4: Search & Filter
```python
# Find available sedans
sedans = system.search_vehicles(category='sedan', available_only=True)

# Find budget vehicles
cheap = system.search_vehicles(max_price=100.0)

# Find loyal customers
vip = system.search_customers(min_rentals=10)
```

## System Architecture

```
CarRentalSystem (Main Orchestrator)
│
├── Vehicles Dictionary
│   ├── Car (instances)
│   ├── Truck (instances)
│   └── Motorcycle (instances)
│
├── Customers Dictionary
│   └── Customer (instances)
│
└── Rentals Dictionary
    └── Rental (instances linking customer + vehicle)
```

## Testing

All 28 unit tests pass:
- 4 Vehicle tests
- 3 Customer tests
- 6 Rental tests
- 12 System tests
- 3 Advanced scenario tests

Run tests:
```bash
python -m unittest test_system -v
```

## Future Enhancements

- Database persistence (SQLite/PostgreSQL)
- Web API (Flask/FastAPI)
- GUI interface (PyQt/Tkinter)
- Payment processing
- Insurance options
- GPS tracking
- Damage assessment
- Customer ratings
- Fleet optimization

## Requirements

- Python 3.6+
- No external dependencies (uses only Python stdlib)

## Author

Developed for Advanced Python Programming Course - Semester 5

## License

Educational Project

---

**Quick Links:**
- [Full Documentation](README.md)
- [Unit Tests](test_system.py)
- [Demo Script](main.py)
