from fastapi import APIRouter, HTTPException
import httpx
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict


carts_router = APIRouter()
products_router = APIRouter()
user_router = APIRouter()
## ejecutar api fastapi dev get_api.py
FAKESTORE_URL = "https://fakestoreapi.com"


## CLASSS APIS

## lista de dellates includios de los productos, como el id del producto y la cantidad del producto
class DetailProduct(BaseModel):
    productId: int
    quantity: int

class DetailCart(BaseModel):
    id: int
    userId: int
    date: datetime
    products: List[DetailProduct]
    __v: int


##✅ 1. Consumir datos externos

## SOLICIUTD DE FUNCION DIRECTAS A API PARA MIRAR LOS PRODUCTOS EXITESNTES
@products_router.get("/products")
async def get_all_product():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{FAKESTORE_URL}/products")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
        


   
        
##✅ 2. Procesar los datos (análisis de ventas lentas)


## ✅2.1 Obtener todos los carritos.
all_carts = []

@carts_router.get("/carts")
async def save_get_all_carts():
    async with httpx.AsyncClient() as client:
        try:
            reponse = await client.get(f"{FAKESTORE_URL}/carts")
            reponse.raise_for_status()
            all_carts.append(reponse.json())  # Usar append para agregar el único elemento
            return all_carts
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")


## ✅2.2 Contar cuántas veces aparece cada producto + sumatoria de todas las ventas + ✅2.3 las veces con mas frecuencia por productoId

count_product = []

@carts_router.get("/countProducts")
async def get_product_counts_carts():
    product_counts: Dict[int, Dict[str, int]] = {}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{FAKESTORE_URL}/carts")
            response.raise_for_status()
            carts = response.json()

            for cart in carts:  # ya no recorremos cart_group, solo carts directamente
                products = cart.get("products", [])
                for product in products:
                    product_id = product.get("productId")
                    quantity = product.get("quantity", 0)
                    if product_id is not None:
                        if product_id not in product_counts:
                            product_counts[product_id] = {
                                "values_found_quantity": 0,
                                "total_quantity": 0
                            }
                        product_counts[product_id]["values_found_quantity"] += 1
                        product_counts[product_id]["total_quantity"] += quantity

            return product_counts

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
        

## ✅2.4 Exponer esos resultados como “ventas lentas”.
VENTA_LENTA_MAXIMA = 2  # 👈 DEFINIDA AQU

@carts_router.get("/slowSales")
async def get_slow_sales_carts():
    product_counts: Dict[int, Dict[str, int]] = {}

    async with httpx.AsyncClient() as client:
        try:
            # Traemos los carritos
            carts_response = await client.get(f"{FAKESTORE_URL}/carts")
            carts_response.raise_for_status()
            carts = carts_response.json()

            # Contamos productos
            for cart in carts:
                products = cart.get("products", [])
                for product in products:
                    product_id = product.get("productId")
                    quantity = product.get("quantity", 0)
                    if product_id is not None:
                        if product_id not in product_counts:
                            product_counts[product_id] = {
                                "values_found_quantity": 0,
                                "total_quantity": 0
                            }
                        product_counts[product_id]["values_found_quantity"] += 1
                        product_counts[product_id]["total_quantity"] += quantity

            # Traemos los productos para buscar sus nombres y categorías
            products_response = await client.get(f"{FAKESTORE_URL}/products")
            products_response.raise_for_status()
            products_list = products_response.json()

            # Creamos un mapa rápido de id -> producto
            product_info = {prod["id"]: prod for prod in products_list}

            # Ahora filtramos las ventas lentas
            slow_sales: List[Dict[str, int]] = []
            for product_id, data in product_counts.items():
                if data["total_quantity"] <= VENTA_LENTA_MAXIMA:
                    product = product_info.get(product_id)
                    if product:
                        slow_sales.append({
                            "title": product.get("title"),
                            "category": product.get("category"),
                            "productId": product_id,
                            "values_found_quantity": data["values_found_quantity"],
                            "times_sold_quanty": data["total_quantity"]
                        })

            return slow_sales

        except Exception as e:
            print("Error:", str(e))  # 👈 para debug
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
        

#✅ 3. Crear un endpoint para mostrar los productos con pocas ventas
#Este endpoint podría ser /slow-products y devolver los productos ordenados por menos ventas.

@carts_router.get("/slow-products")
async def prodcut_slow_carts():
    product_counts: Dict[int, Dict[str, int]] = {}
    async with httpx.AsyncClient() as client:
        try:
            carts_response = await client.get(f"{FAKESTORE_URL}/carts")
            carts_response.raise_for_status()
            carts = carts_response.json()
            # Contamos productos
            for cart in carts:
                products = cart.get("products", [])
                for product in products:
                    product_id = product.get("productId")
                    quantity = product.get("quantity", 0)
                    if product_id is not None:
                        if product_id not in product_counts:
                            product_counts[product_id] = {
                                "total_quantity": 0
                            }
                        product_counts[product_id]["total_quantity"] += quantity
            

            # Traemos los productos para buscar sus nombres y categorías
            products_response = await client.get(f"{FAKESTORE_URL}/products")
            products_response.raise_for_status()
            products_list = products_response.json()

            # Creamos un mapa rápido de id -> producto
            product_info = {prod["id"]: prod for prod in products_list}

            # Ahora filtramos las ventas lentas
            slow_products: List[Dict[str, int]] = []
            for product_id, data in product_counts.items():
                    product = product_info.get(product_id)
                    if product:
                        slow_products.append({
                            "title": product.get("title"),
                            "category": product.get("category"),
                            "productId": product_id,
                            "sale_quantity": data["total_quantity"]
                        })
            
            # Ordenamos de menor a mayor por sale_quantity
            slow_products.sort(key=lambda x: x["sale_quantity"])

            return slow_products

        except Exception as e:
            print("Error:", str(e))  # 👈 para debug
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
        



























## SOLICIUTD DE FUNCION DIRECTAS A API PARA MIRAR LOS USUARIOS  EXITESNTES
@user_router.get("/users")
async def get_all_users():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{FAKESTORE_URL}/users")
            response.raise_for_status()
            print(response.json)
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
        
