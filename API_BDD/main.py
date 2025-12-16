"""
Module principal de l'API (Application Programming Interface).

Ce module initialise l'application FastAPI, configure les routes (endpoints)
et gère l'interaction entre les requêtes HTTP, la validation Pydantic
et la persistance des données via SQLAlchemy.
"""
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

import model
import schemas as schema
from database import engine, get_db
from Classes.Vehicule import Vehicule 

model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Car Rental API",
    description="API de gestion de location de voitures avec base de données SQLite",
    version="1.0"
)

@app.post("/vehicles", response_model=schema.VehicleResponse, tags=["Vehicles"])
def add_vehicle(vehicle: schema.VehicleCreate, db: Session = Depends(get_db)):
    """
    Ajouter un nouveau véhicule à la flotte.

    Cette fonction crée une entrée dans la table 'vehicles'.
    L'état initial du véhicule est défini automatiquement sur 'available' 
    en utilisant la constante métier `Vehicule.AVAILABLE`.

    Args:
        vehicle (schema.VehicleCreate): Les données du véhicule à créer.
        db (Session): La session de base de données injectée.

    Returns:
        DBVehicle: L'objet véhicule créé et persisté.
    """
    db_vehicle = model.DBVehicle(
        brand=vehicle.brand,
        model=vehicle.model,
        category=vehicle.category,
        daily_rate=vehicle.daily_rate,
        num_doors=vehicle.num_doors,
        fuel_type=vehicle.fuel_type,
        payload_capacity=vehicle.payload_capacity,
        engine_cc=vehicle.engine_cc,
        state=Vehicule.AVAILABLE 
    )
    
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@app.get("/vehicles", response_model=List[schema.VehicleResponse], tags=["Vehicles"])
def get_vehicles(available_only: bool = False, db: Session = Depends(get_db)):
    """
    Lister les véhicules de la flotte.

    Args:
        available_only (bool): Si True, filtre pour ne renvoyer que les véhicules
        dont l'état est 'available'.
        db (Session): La session de base de données injectée.

    Returns:
        List[DBVehicle]: Une liste d'objets véhicules.
    """
    query = db.query(model.DBVehicle)
    
    if available_only:
        query = query.filter(model.DBVehicle.state == Vehicule.AVAILABLE)
        
    return query.all()

@app.post("/customers", response_model=schema.CustomerResponse, tags=["Customers"])
def add_customer(customer: schema.CustomerCreate, db: Session = Depends(get_db)):
    """
    Enregistrer un nouveau client dans le système.

    Args:
        customer (schema.CustomerCreate): Les informations personnelles du client
        et son type de permis.
        db (Session): La session de base de données injectée.

    Returns:
        DBCustomer: Le client créé.
    """
    db_customer = model.DBCustomer(
        first_name=customer.first_name,
        last_name=customer.last_name,
        age=customer.age,
        license_type=customer.license_type
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.get("/customers", response_model=List[schema.CustomerResponse], tags=["Customers"])
def get_customers(db: Session = Depends(get_db)):
    """
    Récupérer la liste complète des clients enregistrés.

    Args:
        db (Session): La session de base de données injectée.

    Returns:
        List[DBCustomer]: La liste de tous les clients.
    """
    return db.query(model.DBCustomer).all()

@app.post("/rentals", response_model=schema.RentalResponse, tags=["Rentals"])
def create_rental(rental: schema.RentalCreate, db: Session = Depends(get_db)):
    """
    Créer une nouvelle location (Transaction complexe).

    Cette méthode effectue une série de validations métier avant de créer la location :
    1. Vérifie l'existence du véhicule et du client.
    2. Vérifie la disponibilité du véhicule (doit être 'available').
    3. Vérifie la cohérence des dates (début < fin).
    4. Vérifie l'éligibilité du client (Permis et Âge) selon la catégorie du véhicule :
    - Voiture/Van : 17+ et Permis B ou C.
    - Camion : 21+ et Permis C.
    - Moto : 18+ et Permis A.
    
    Si toutes les conditions sont réunies, le coût initial est calculé,
    l'état du véhicule passe à 'rented', et la location est sauvegardée.

    Args:
        rental (schema.RentalCreate): Les IDs et les dates de la location.
        db (Session): La session de base de données injectée.

    Raises:
        HTTPException: Si une des règles métier n'est pas respectée (400 ou 404).

    Returns:
        DBRental: L'objet location créé avec le statut 'active'.
    """
    vehicle = db.query(model.DBVehicle).filter(model.DBVehicle.vehicle_id == rental.vehicle_id).first()
    customer = db.query(model.DBCustomer).filter(model.DBCustomer.customer_id == rental.customer_id).first()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
        
    if vehicle.state != Vehicule.AVAILABLE:
        raise HTTPException(status_code=400, detail=f"Vehicle is currently {vehicle.state}")

    if rental.start_date >= rental.end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date")

    if vehicle.category in ['car', 'van']:
        if customer.age < 18 or customer.license_type not in ['B', 'C']:
            raise HTTPException(status_code=400, detail="Customer not eligible (Age 18+ and License B required)")
    
    elif vehicle.category == 'truck':
        if customer.age < 21 or customer.license_type != 'C':
            raise HTTPException(status_code=400, detail="Customer not eligible (Age 21+ and License C required)")
    
    elif vehicle.category in ['bike', 'scooter']:
        if customer.age < 18 or customer.license_type != 'A':
            raise HTTPException(status_code=400, detail="Customer not eligible (Age 18+ and License A required)")

    duration = (rental.end_date - rental.start_date).days
    if duration < 1: duration = 1
    initial_cost = duration * vehicle.daily_rate
    
    db_rental = model.DBRental(
        customer_id=customer.customer_id,
        vehicle_id=vehicle.vehicle_id,
        start_date=rental.start_date,
        end_date=rental.end_date,
        status="active",
        total_cost=initial_cost,
        penalty=0.0
    )
    
    vehicle.state = Vehicule.RENTED
    
    db.add(db_rental)
    db.commit()
    db.refresh(db_rental)
    
    return db_rental

@app.post("/rentals/{rental_id}/complete", response_model=schema.RentalResponse, tags=["Rentals"])
def complete_rental(rental_id: int, db: Session = Depends(get_db)):
    """
    Terminer une location et retourner le véhicule.

    Cette méthode :
    1. Enregistre la date de retour réelle (maintenant).
    2. Change le statut de la location à 'completed'.
    3. Vérifie s'il y a un retard par rapport à la date de fin prévue.
    4. Si retard : Calcule une pénalité (50% du tarif journalier par jour de retard)
    et l'ajoute au coût total.
    5. Libère le véhicule (le remet à l'état 'available').

    Args:
        rental_id (int): L'ID de la location à clôturer.
        db (Session): La session de base de données injectée.

    Raises:
        HTTPException: Si la location n'existe pas ou n'est pas active.

    Returns:
        DBRental: L'objet location mis à jour avec le coût final et les pénalités.
    """
    rental = db.query(model.DBRental).filter(model.DBRental.rental_id == rental_id).first()
    
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    
    if rental.status != "active":
        raise HTTPException(status_code=400, detail="Rental is not active")
    
    return_date = datetime.now()
    rental.actual_return_date = return_date
    rental.status = "completed"
    
    vehicle = rental.vehicle 
    
    if return_date > rental.end_date:
        overdue_days = (return_date - rental.end_date).days
        if overdue_days > 0:
            penalty_amount = overdue_days * (vehicle.daily_rate * 0.5)
            rental.penalty = penalty_amount
            rental.total_cost += penalty_amount

    vehicle.state = Vehicule.AVAILABLE
    
    db.commit()
    db.refresh(rental)
    
    return rental