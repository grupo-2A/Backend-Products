# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexión a PostgreSQL
DATABASE_URL = "postgresql://jhon_dev:123456@localhost/productsdb"

# Crear el engine
engine = create_engine(DATABASE_URL)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarar Base
Base = declarative_base()

