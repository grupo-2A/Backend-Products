# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexión a PostgreSQL (puedes usar variables de entorno para mayor seguridad)
DATABASE_URL = "postgresql://jhon_dev:123456@localhost/productsdb"

# Crear el engine
engine = create_engine(DATABASE_URL, echo=False)  # Usa echo=True si quieres ver las queries en consola

# Crear la sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarar Base para modelos
Base = declarative_base()


