from pydantic import BaseModel

# -------- MODELOS DE CATEGORÍA --------
class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int

    class Config:
        from_attributes = True


# -------- MODELOS DE PRODUCTO --------
class ProductoBase(BaseModel):
    nombre: str
    cantidad: int
    precio: float            # ✅ Añadido aquí
    categoria_id: int

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int

    class Config:
        from_attributes = True



