from fastapi import FastAPI
from routers.products import productos  # importas tus routers
from routers.carts import carst
from routers.analytics import activaracanisis

app = FastAPI(
    title="API de Análisis de Ventas",
    description="Cruce de productos y carritos para análisis",
    version="1.0.0"
)

# Registrar los routers
app.include_router(productos, prefix="/products", tags=["Products"])
app.include_router(carst, prefix="/carts", tags=["Carts"])
app.include_router(activaracanisis, prefix="/analytics", tags=["Analytics"])


# Opcional: Ruta raíz
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de análisis de ventas"}
