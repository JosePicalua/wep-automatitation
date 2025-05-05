# 📊 Web Automation for Data Analytics

Este proyecto automatiza la recolección, procesamiento y análisis de datos desde una API simulada utilizando **FastAPI**. Está orientado a Data Analysts que necesitan estructurar pipelines rápidos de extracción y evaluación de productos y carritos de compras. 

## 🚀 Descripción

A través de esta aplicación web:

- Se consumen datos de productos y carritos desde [`https://dummyjson.com`](https://dummyjson.com).
- Se procesan y transforman los datos en rutas accesibles para análisis.
- Se realiza un cruce entre productos y carritos para determinar ventas altas o bajas por producto.

## 🧠 Objetivo

Este proyecto tiene como fin mostrar cómo integrar automatización web (web scraping/API requests) con análisis de datos para construir un backend útil en decisiones analíticas.

## 🏗️ Estructura del Proyecto

proyecto_web_scraping/
│
├── app/
│ ├── routers/
│ │ ├── products.py # Ruta /products → obtiene productos
│ │ ├── carts.py # Ruta /carts → obtiene carritos
│ │ └── analytics.py # Ruta /analytics/slow_sales → lógica de análisis
│ ├── services/
│ │ └── analytics_service.py # Cruce de carritos con productos para análisis
│ └── main.py # Punto de entrada FastAPI
│
├── requirements.txt # Dependencias del proyecto
├── README.md # Este archivo

## 🔍 Endpoints Disponibles

| Método | Ruta                      | Descripción                                               |
|--------|---------------------------|-----------------------------------------------------------|
| GET    | `/products`               | Devuelve todos los productos con datos clave.             |
| GET    | `/carts`                  | Devuelve los carritos con detalles de productos.          |
| GET    | `/analytics/slow_sales`  | Analiza ventas por producto y clasifica su rendimiento.   |


🧪 Instalación y Uso
Clona este repositorio:

git clone https://github.com/JosePicalua/web_scraping.git
cd proyecto_web_scraping


Crea un entorno virtual e instala las dependencias:

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt


uvicorn app.main:app --reload

Visita http://127.0.0.1:8000/docs para acceder a la documentación interactiva Swagger.

🛠️ Tecnologías Usadas
FastAPI: Framework para construir APIs rápidas y modernas.

HTTPX: Cliente HTTP asincrónico.

Pydantic: Validación de datos.

DummyJSON API: Fuente simulada de datos de ecommerce.

💡 Ideal para
Analistas de Datos que deseen automatizar consultas a APIs.

Demostraciones de análisis cruzado para fines venta,compras,tasas interes,fraude,inventario.

Practicar consumo y análisis de APIs RESTful.

📌 Notas
Esta API es de uso educativo/demo, no para entornos de producción.

Los datos se obtienen de una fuente simulada, no en tiempo real.

Desarrollado con 💻 por [@JosePicalua]


### Ejemplo de salida `/analytics/slow_sales`:
```json
{
  "productos": [
    {
      "product": {
        "id": 1,
        "title": "iPhone 9",
        "category": "smartphones"
      },
      "ventas_totales": 18,
      "promedio_por_carrito": 6,
      "ventas": [...],
      "nivel_ventas": "BAJA"
    }
  ]
}

