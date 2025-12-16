from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class DBVehicle(Base):
    """
    Modèle SQLAlchemy représentant la table 'vehicles' dans la base de données.

    Cette classe utilise une stratégie de table unique (Single Table Inheritance) 
    pour stocker tous les types de véhicules (Voiture, Camion, Moto). 
    Les attributs spécifiques à certains types sont définis comme 'nullable'.

    Attributes:
        id (int): Clé primaire unique du véhicule.
        brand (str): Marque du véhicule.
        model (str): Modèle du véhicule.
        category (str): Catégorie du véhicule ('car', 'truck', 'bike', etc.).
        daily_rate (float): Tarif journalier de location.
        state (str): État actuel du véhicule ('available', 'rented', 'maintenance').
        num_doors (int, optional): Nombre de portes (Spécifique aux voitures).
        fuel_type (str, optional): Type de carburant (Spécifique aux voitures).
        payload_capacity (float, optional): Capacité de chargement en tonnes (Spécifique aux camions).
        engine_cc (int, optional): Cylindrée du moteur (Spécifique aux motos).
        rentals (relationship): Relation One-to-Many vers la table des locations.
    """
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String)
    model = Column(String)
    category = Column(String)
    daily_rate = Column(Float)
    state = Column(String, default="available")
    
    num_doors = Column(Integer, nullable=True)
    fuel_type = Column(String, nullable=True)
    payload_capacity = Column(Float, nullable=True)
    engine_cc = Column(Integer, nullable=True)

    rentals = relationship("DBRental", back_populates="vehicle")

class DBCustomer(Base):
    """
    Modèle SQLAlchemy représentant la table 'customers' dans la base de données.

    Stocke les informations personnelles et les détails du permis de conduire
    des clients enregistrés.

    Attributes:
        id (int): Clé primaire unique du client.
        first_name (str): Prénom du client.
        last_name (str): Nom de famille du client.
        age (int): Âge du client (utilisé pour vérifier l'éligibilité).
        license_type (str): Type de permis de conduire ('A', 'B', 'C').
        rentals (relationship): Relation One-to-Many vers l'historique des locations du client.
    """
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    license_type = Column(String)

    rentals = relationship("DBRental", back_populates="customer")

class DBRental(Base):
    """
    Modèle SQLAlchemy représentant la table 'rentals' dans la base de données.

    Cette table agit comme une table de liaison entre les Clients et les Véhicules,
    tout en stockant les détails temporels et financiers de la transaction.

    Attributes:
        id (int): Clé primaire unique de la location.
        customer_id (int): Clé étrangère liant au client.
        vehicle_id (int): Clé étrangère liant au véhicule.
        start_date (datetime): Date de début de la location.
        end_date (datetime): Date de fin prévue de la location.
        actual_return_date (datetime, optional): Date réelle de retour du véhicule.
        status (str): État de la location ('active', 'completed', 'cancelled').
        total_cost (float): Coût total facturé (location + pénalités éventuelles).
        penalty (float): Montant spécifique des pénalités de retard.
        customer (relationship): Objet client associé.
        vehicle (relationship): Objet véhicule associé.
    """
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    actual_return_date = Column(DateTime, nullable=True)
    status = Column(String, default="active")
    total_cost = Column(Float, default=0.0)
    penalty = Column(Float, default=0.0)

    customer = relationship("DBCustomer", back_populates="rentals")
    vehicle = relationship("DBVehicle", back_populates="rentals")