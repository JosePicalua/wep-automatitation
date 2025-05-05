import httpx

APIMERCADOLIBRE = "https://dummyjson.com"

async def analizar_ventas_por_producto_B_A():
    async with httpx.AsyncClient() as client:
        productos = await client.get(f"{APIMERCADOLIBRE}/products")
        carritos = await client.get(f"{APIMERCADOLIBRE}/carts")

        productos.raise_for_status()
        carritos.raise_for_status()

        all_products = productos.json().get("products", [])
        all_carts = carritos.json().get("carts", [])

        # 1. Armar índice de ventas
        ventas_por_producto = {}
        for cart in all_carts:
            for producto in cart.get("products", []):
                pid = producto["id"]
                ventas_por_producto.setdefault(pid, []).append({
                    "cart_id": cart["id"],
                    "title": producto["title"],
                    "price": producto["price"],
                    "quantity": producto["quantity"],
                    "total": producto["total"]
                })

        resultado_avg = {
            "productos": []
        }

        # 2. Analizar por producto
        for producto in all_products:
            pid = producto["id"]
            ventas = ventas_por_producto.get(pid, [])
            total_vendido = sum(v["quantity"] for v in ventas)
            cantidad_registros = len(ventas)
            promedio = total_vendido / cantidad_registros if cantidad_registros > 0 else 0

            resultado_avg["productos"].append({
                "product": {
                    "id": pid,
                    "title": producto["title"],
                    "category": producto["category"]
                },
                "ventas_totales": total_vendido,
                "promedio_por_carrito": promedio,
                "ventas": ventas,
                "nivel_ventas": "ALTA" if total_vendido > promedio else "BAJA"
            })

        return resultado_avg
