# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Le nom du fichier qui sera créé
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db" # Créera le fichier dans API_BDD/

# Création du moteur (le connecteur)
# connect_args={"check_same_thread": False} est nécessaire uniquement pour SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Création de la session (l'outil pour faire des requêtes)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# La classe de base pour nos modèles (tables)
Base = declarative_base()

# Fonction utilitaire pour obtenir la DB dans les routes FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()