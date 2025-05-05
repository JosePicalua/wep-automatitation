from fastapi import APIRouter
from services.analytics_service import  analizar_ventas_por_producto_B_A

activaracanisis = APIRouter()


## SE QUITA EL PREFICO / DADO QUE EN LA FUNCION QUESE CREA EN EL MODULO analytics_service va directo
@activaracanisis.get("")
async def avg_sales():
    return await analizar_ventas_por_producto_B_A()

