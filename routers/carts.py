from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any
import httpx



APIMERCADOLIBRE = "https://dummyjson.com"

## 1. Ventas lentas

carst = APIRouter()


### CARTS
## SE QUITA EL PREFIJO /carts YA QUE EN EL MAIN ESTA DEFINIDO EL PREFICO POR EL APIROUTRESS
@carst.get("")
async def get_all_cart():
    global_analitycs_carts: Dict[str, List[Dict[str, Any]]] = {
        "carts": []
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{APIMERCADOLIBRE}/carts")
            response.raise_for_status()
            data = response.json()

            carts = data.get("carts", [])

            for cart in carts:
                id_cart = cart.get("id")
                products = cart.get("products", [])

                processed_products = []
                for product in products:
                    processed_product = {
                        "id": product.get("id"),
                        "title": product.get("title"),
                        "price": product.get("price"),
                        "quantity": product.get("quantity"),
                        "total": product.get("total"),
                        "discountPercentage": product.get("discountPercentage"),
                        "discountedTotal": product.get("discountedTotal")
                    }
                    processed_products.append(processed_product)

                global_analitycs_carts["carts"].append({
                    "id": id_cart,
                    "products": processed_products
                })

            return global_analitycs_carts

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    
