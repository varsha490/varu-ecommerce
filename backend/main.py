from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List
from models import Product, Order
import json
import os

app = FastAPI(title="Varu E-commerce API")

# Setup CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load products once at startup
products_cache = []

def load_products():
    global products_cache
    if products_cache:
        return products_cache
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "products.json")
        with open(file_path, "r") as f:
            data = json.load(f)
            # Map 'image' to 'image_url' for frontend compatibility
            for item in data:
                if 'image' in item and 'image_url' not in item:
                    item['image_url'] = item['image']
            products_cache = data
            return data
    except Exception as e:
        print(f"Error loading products: {e}")
        return []

# Ensure products are loaded
load_products()

VIRTUAL_DB_ORDERS = []

@app.get("/api/products", response_model=List[Product])
def get_products():
    return load_products()

@app.get("/api/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    products = load_products()
    for p in products:
        if p.get("id") == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/api/orders", response_model=Order)
def create_order(order: Order):
    order.id = len(VIRTUAL_DB_ORDERS) + 1
    VIRTUAL_DB_ORDERS.append(order)
    return order

# Static files for React frontend
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")

if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")

    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        # Fallback to index.html for React Router
        index_path = os.path.join(frontend_dist, "index.html")
        return FileResponse(index_path)
else:
    @app.get("/")
    def read_root():
        return {"message": "Welcome to Varu E-commerce API (Frontend not built)"}
