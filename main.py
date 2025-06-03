from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal, Base


# Crear las tablas automáticamente al iniciar
Base.metadata.create_all(bind=engine)



app = FastAPI()



# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





@app.get("/")
def index():
    return {"message" : "API productos"}





# -------- RUTAS PARA CATEGORÍAS --------

@app.post("/categorias/", response_model=schemas.Categoria)
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    # Verificar que no exista otra categoría con el mismo nombre
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
    # Verificar si ya existe otra categoría con el nuevo nombre
    dup = db.query(models.Categoria)\
            .filter(models.Categoria.nombre == datos.nombre, models.Categoria.id != categoria_id)\
            .first()
    if dup:
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
    # Antes de eliminar, podrías comprobar si hay productos asociados
    productos_asoc = db.query(models.Producto).filter(models.Producto.categoria_id == categoria_id).first()
    if productos_asoc:
        raise HTTPException(status_code=400, detail="No se puede eliminar: hay productos asociados")
    db.delete(cat_db)
    db.commit()
    return {"message": "Categoría eliminada correctamente"}



# -------- RUTAS PARA PRODUCTOS --------

@app.post("/productos/", response_model=schemas.Producto)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    categoria = db.query(models.Categoria).filter(models.Categoria.id == producto.categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db_producto = models.Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto



@app.get("/productos/", response_model=list[schemas.Producto])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(models.Producto).all()