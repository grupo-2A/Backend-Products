from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import models, schemas
from database import engine, SessionLocal, Base

# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)

# Inicializar la app
app = FastAPI()

# CORS para frontend
origins = [
    "http://localhost:5173",  # Cambia según la URL de tu frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta raíz
@app.get("/")
def index():
    return {"message": "API productos"}

# -------- RUTAS DE CATEGORÍAS --------
@app.post("/categorias/", response_model=schemas.Categoria)
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    existe = db.query(models.Categoria).filter(models.Categoria.nombre == categoria.nombre).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre")
    nueva = models.Categoria(nombre=categoria.nombre)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@app.get("/categorias/", response_model=list[schemas.Categoria])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(models.Categoria).all()

@app.get("/categorias/{categoria_id}", response_model=schemas.Categoria)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    cat = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return cat

@app.put("/categorias/{categoria_id}", response_model=schemas.Categoria)
def actualizar_categoria(categoria_id: int, datos: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    cat_db = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not cat_db:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    duplicado = db.query(models.Categoria).filter(
        models.Categoria.nombre == datos.nombre,
        models.Categoria.id != categoria_id
    ).first()
    if duplicado:
        raise HTTPException(status_code=400, detail="Otra categoría ya usa ese nombre")
    cat_db.nombre = datos.nombre
    db.commit()
    db.refresh(cat_db)
    return cat_db

@app.delete("/categorias/{categoria_id}")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    cat_db = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not cat_db:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    productos_asoc = db.query(models.Producto).filter(models.Producto.categoria_id == categoria_id).first()
    if productos_asoc:
        raise HTTPException(status_code=400, detail="No se puede eliminar: hay productos asociados")
    db.delete(cat_db)
    db.commit()
    return {"message": "Categoría eliminada correctamente"}

# -------- RUTAS DE PRODUCTOS --------
@app.post("/productos/", response_model=schemas.Producto)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    categoria = db.query(models.Categoria).filter(models.Categoria.id == producto.categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    nuevo_producto = models.Producto(
        nombre=producto.nombre,
        cantidad=producto.cantidad,
        precio=producto.precio,  # ← Aseguramos que se incluya
        categoria_id=producto.categoria_id
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto


@app.get("/productos/", response_model=list[schemas.Producto])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(models.Producto).all()

@app.get("/productos/{producto_id}", response_model=schemas.Producto)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.put("/productos/{producto_id}", response_model=schemas.Producto)
def actualizar_producto(producto_id: int, datos: schemas.ProductoCreate, db: Session = Depends(get_db)):
    prod_db = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not prod_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    categoria = db.query(models.Categoria).filter(models.Categoria.id == datos.categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    # Actualizar datos, incluyendo el precio
    prod_db.nombre = datos.nombre
    prod_db.cantidad = datos.cantidad
    prod_db.precio = datos.precio  # ← Añadido
    prod_db.categoria_id = datos.categoria_id

    db.commit()
    db.refresh(prod_db)
    return prod_db


@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    prod_db = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not prod_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(prod_db)
    db.commit()
    return {"message": "Producto eliminado correctamente"}
