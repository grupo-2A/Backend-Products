from pydantic import BaseModel

class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int
    class Config:
        orm_mode = True

class ProductoBase(BaseModel):
    nombre: str
    cantidad: int
    categoria_id: int

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    class Config:
        orm_mode = True
