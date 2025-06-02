from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)

    productos = relationship("Producto", back_populates="categoria")