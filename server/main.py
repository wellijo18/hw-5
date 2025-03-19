# =========================================== imports =============================================

from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import asyncpg

# ======================================== database setup =========================================

# Database connection details
DATABASE_URL = "postgresql://p_user:p_password@localhost:5432/product_db"

# Establishing a connection to the database
async def connect(): return await asyncpg.connect(DATABASE_URL)

# Context manager to handle the database connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = await connect()
    try: yield
    finally: await app.state.db.close()

# =========================================== app setup ===========================================

# Creating a FastAPI instance
app = FastAPI(lifespan=lifespan)

# Setting up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================ routing  ===========================================

# root route, testing that the connection to the database works
@app.get("/")
async def root():
    try:
        await app.state.db.execute("SELECT 1")
        return {"message": "Hello World! Database connection is successful."}
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Bye World! Database connection failed.")

@app.get("/products/count")
async def get_prodcount():
    try:
        result = await app.state.db.fetchval("SELECT COUNT(*) FROM products")
        return {"product_count": result}
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="failed to get count")

@app.get("/products")
async def get_prods(page: int = 1, limit: int = 10):
    try:
        products = await app.state.db.fetch("SELECT * FROM products LIMIT $1 OFFSET $2", limit, offset=(page - 1) * limit)
        result = [dict(daProduct) for daProduct in products]
        return {"products": result, "page": page, "limit": limit}
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="failed to get products")


@app.get("/products/{product_id}")
async def get_pid(product_id: int):
    try:
        product = await app.state.db.fetchrow("SELECT * FROM products WHERE id = $1", product_id)
        if not product:
            raise HTTPException(status_code=404, detail="cant find product")
        return dict(product)
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="failed to get product")

# ======================================== run the app =========================================
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)

# ==============================================================================================
