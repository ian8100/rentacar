from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class VehicleCreate(BaseModel):
    """
    Modèle d'entrée pour l'ajout d'un véhicule.
    
    Ce modèle est polymorphique : il contient tous les champs possibles pour 
    les trois types de véhicules (Voiture, Camion, Moto). 
    Seuls les champs pertinents pour la 'category' choisie doivent être remplis.
    """
    brand: str
    model: str
    category: str 
    daily_rate: float

    num_doors: Optional[int] = 4       
    fuel_type: Optional[str] = "petrol" 
    payload_capacity: Optional[float] = 18.0
    engine_cc: Optional[int] = 500    

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "brand": "Toyota",
            "model": "Corolla",
            "category": "car",
            "daily_rate": 50.0,
            "num_doors": 4,
            "fuel_type": "hybrid"
        }
    })


class VehicleResponse(BaseModel):
    """
    Modèle de sortie pour l'affichage d'un véhicule.
    
    Inclut l'ID généré par la base de données et l'état actuel (state),
    qui sont gérés par le système et non par l'utilisateur lors de la création.
    """
    vehicle_id: int
    brand: str
    model: str
    category: str
    daily_rate: float
    state: str
    model_config = ConfigDict(from_attributes=True)


class CustomerCreate(BaseModel):
    """
    Modèle d'entrée pour l'enregistrement d'un client.
    """
    first_name: str
    last_name: str
    age: int
    license_type: str 


class CustomerResponse(BaseModel):
    """
    Modèle de sortie pour l'affichage d'un client.
    Renvoie l'ID unique du client.
    """
    customer_id: int
    first_name: str
    last_name: str
    license_type: str

    model_config = ConfigDict(from_attributes=True)

class RentalCreate(BaseModel):
    """
    Modèle d'entrée pour créer une réservation.
    
    Attend les ID du client et du véhicule, ainsi que les dates.
    Format des dates attendu : ISO 8601 (YYYY-MM-DDTHH:MM:SS) ou (YYYY-MM-DD).
    """
    customer_id: int
    vehicle_id: int
    start_date: datetime
    end_date: datetime


class RentalResponse(BaseModel):
    """
    Modèle de sortie pour une confirmation de location.
    Indique le statut et le coût (initial ou final).
    """
    rental_id: int
    status: str
    total_cost: float

    model_config = ConfigDict(from_attributes=True)