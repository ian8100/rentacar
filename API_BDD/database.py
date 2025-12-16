"""
Configuration de la base de données (Database Setup).

Ce module initialise la connexion à la base de données SQLite via SQLAlchemy.
Il définit :
1. L'URL de connexion.
2. Le moteur (Engine) qui gère la communication avec le fichier SQL.
3. La Session (SessionLocal) qui sera instanciée pour chaque requête.
4. La classe de base (Base) dont hériteront tous les modèles (tables).
5. La dépendance (get_db) pour l'injection dans les routes FastAPI.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Générateur de session de base de données (Dependency).

    Cette fonction est conçue pour être utilisée avec `Depends` dans FastAPI.
    Elle crée une nouvelle session de base de données pour chaque requête HTTP,
    la transmet à la fonction de route via `yield`, et s'assure que la session
    est correctement fermée (via `finally`) une fois la requête terminée, 
    même si une erreur survient.

    Yields:
        Session: Une instance active de session SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()