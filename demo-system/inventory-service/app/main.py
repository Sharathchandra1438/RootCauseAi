import logging
import time

from fastapi import FastAPI, HTTPException, Request

from app.logger import get_logger

app = FastAPI(title="inventory-service")
logger = get_logger()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    fields = {"method": request.method, "path": request.url.path}

    try:
        response = await call_next(request)
    except Exception:

        fields["status"] = 500
        fields["latency_ms"] = round((time.perf_counter() - start)*1000, 2)
        logger.exception("request failed", extra={"fields": fields})
        raise

    fields["status"] = response.status_code
    fields["latency_ms"] = round((time.perf_counter() - start)*1000, 2)

    if response.status_code >= 500:
        level = logging.ERROR
    elif response.status_code >= 400:
        level = logging.WARNING
    else:
        level = logging.INFO

    logger.log(level, "request handled", extra={"fields": fields})
    return response


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