from fastapi import FastAPI, HTTPException

app = FastAPI(title="inventory-service")

PRODUCTS = {
    1: {"id":1,"name":"Keyboard","price":1500,"stock":20},
    2: {"id":2, "name":"Mouse","price": 600, "stock":50},
    3: {"id":3, "name":"Monitor", "price": 9000,"stock": 5},
}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/products")
def list_products():
    return list(PRODUCTS.values())

@app.get("/products/{product_id}")
def get_product(product_id : int):
    if product_id not in PRODUCTS:
        raise HTTPException(status_code=404, detail="Product not found")
    return PRODUCTS[product_id]