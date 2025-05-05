from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any
import httpx


APIMERCADOLIBRE = "https://dummyjson.com"
## DIRECTAMENTE A LA API Y ATRACCION DE CATEGORIA, PARA IR DIRECTO PARA DESPUES UNIRLOS
productos = APIRouter()
### PRODUCTOS
## SE QUITA EL PREFIJO /products YA QUE EN EL MAIN ESTA DEFINIDO EL PREFICO POR EL APIROUTRESS
@productos.get("")
async def get_all_products():
    async with httpx.AsyncClient() as client:
        global_product_analitycs_slow: Dict[str, List[Dict[str, Any]]] = {
              ##definicion de la key para saber cual es la estructura del datos
              "products": []}
        try:
            response = await client.get(f"{APIMERCADOLIBRE}/products")
            response.raise_for_status()
            data = response.json()

            productos_request = data.get("products", [])  # ✅ Obtienes solo el campo 'products'
            for product in productos_request:
                            id_producto = product.get("id")
                            name_producto = product.get("title")
                            category = product.get("category")
                            price = product.get("price")
                            discountPercentage = product.get("discountPercentage")
                            rating = product.get("rating")
                            stock = product.get("stock")
                            minimumOrderQuantity = product.get("minimumOrderQuantity")
                            sku = product.get("sku")
                            if id_producto is not None and name_producto is not None:
                                global_product_analitycs_slow["products"].append({
                                    "id": id_producto,
                                    "title": name_producto,
                                    "category": category,
                                    "name": name_producto,
                                    "price": price,
                                    "stock": stock,
                                    "discountPercentage": discountPercentage,
                                    "rating": rating,
                                    "minimumOrderQuantity": minimumOrderQuantity,
                                    "sku": sku,
                                    })

            return global_product_analitycs_slow
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")