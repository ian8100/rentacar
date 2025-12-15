import sys
import os

# 1. Permettre l'import depuis le dossier frère "Classes"
# On ajoute le dossier parent (MonProjetLocation) au chemin de recherche Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

# 2. Imports locaux (Note le changement de nom : model, schemas, database)
import model     
import schemas  
from database import engine, get_db

# 3. Import depuis le dossier Classes (rendu possible grâce au sys.path plus haut)
# Utile si tu veux utiliser Vehicule.AVAILABLE ou Vehicule.RENTED
from Classes.Vehicule import Vehicule 

# Création des tables
model.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- VÉHICULES AVEC DATABASE ---

@app.post("/vehicles", response_model=schemas.VehicleResponse)
def add_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    # Création de l'objet Base de Données
    db_vehicle = model.DBVehicle(
        brand=vehicle.brand,
        model=vehicle.model,
        category=vehicle.category,
        daily_rate=vehicle.daily_rate,
        # Champs optionnels
        num_doors=vehicle.num_doors,
        fuel_type=vehicle.fuel_type,
        payload_capacity=vehicle.payload_capacity,
        engine_cc=vehicle.engine_cc,
        state="available"
    )
    
    # Ajout et sauvegarde
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle) # Récupère l'ID généré automatiquement
    
    # Conversion pour la réponse (mapping DB -> Pydantic)
    # Note: Pydantic s'en charge si les champs ont les mêmes noms
    return  {
        "vehicle_id": db_vehicle.id,
        "brand": db_vehicle.brand,
        "model": db_vehicle.model,
        "category": db_vehicle.category,
        "daily_rate": db_vehicle.daily_rate,
        "state": db_vehicle.state
    }

@app.get("/vehicles", response_model=List[schemas.VehicleResponse])
def get_vehicles(available_only: bool = False, db: Session = Depends(get_db)):
    # Requête SQL via SQLAlchemy
    query = db.query(model.DBVehicle)
    
    if available_only:
        query = query.filter(model.DBVehicle.state == "available")
        
    vehicles = query.all()
    
    # Mapping manuel rapide pour correspondre au schéma de réponse (ou adapter le schéma)
    return [
        {
            "vehicle_id": v.id,
            "brand": v.brand,
            "model": v.model,
            "category": v.category,
            "daily_rate": v.daily_rate,
            "state": v.state
        } 
        for v in vehicles
    ]

# --- LOCATIONS (Exemple avec logique métier) ---

@app.post("/rentals", response_model=schemas.RentalResponse)
def create_rental(rental: schemas.RentalCreate, db: Session = Depends(get_db)):
    # 1. Récupérer le véhicule et le client depuis la DB
    vehicle = db.query(model.DBVehicle).filter(model.DBVehicle.id == rental.vehicle_id).first()
    customer = db.query(model.DBCustomer).filter(model.DBCustomer.id == rental.customer_id).first()
    
    if not vehicle or not customer:
        raise HTTPException(status_code=404, detail="Vehicle or Customer not found")
        
    # 2. Vérifications métier (Disponibilité)
    if vehicle.state != "available":
        raise HTTPException(status_code=400, detail="Vehicle not available")
    
    # (Ici tu pourrais réintégrer tes vérifications d'âge/permis en utilisant les objets récupérés)
    
    # 3. Créer la location
    db_rental = model.DBRental(
        customer_id=customer.id,
        vehicle_id=vehicle.id,
        start_date=rental.start_date,
        end_date=rental.end_date,
        status="active",
        total_cost=0 # Sera calculé à la fin
    )
    
    # 4. Mettre à jour l'état du véhicule
    vehicle.state = "rented"
    
    # 5. Tout sauvegarder (Transaction)
    db.add(db_rental)
    db.commit()
    db.refresh(db_rental)
    
    return {
        "rental_id": db_rental.id,
        "status": db_rental.status,
        "total_cost": db_rental.total_cost
    }