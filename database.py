from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Reemplaza con tus propios datos de conexión
DATABASE_URL = "postgresql://usuario:contraseña@localhost/nombre_base_datos"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
