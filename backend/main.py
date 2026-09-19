from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    description: str

DB = "products.db"

def get_db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL DEFAULT 0,
        description TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()

create_tables()



@app.get("/products")
def get_products() -> list[Product]:
    connection = get_db_connection()
    rows = connection.execute("SELECT * FROM products").fetchall()

    connection.close()

    product_list = []
    for row in rows:
        product = Product(id=row[0], name=row[1], price=row[2], stock=row[3], description=row[4])
        product_list.append(product)


    return product_list

@app.post("/products")
def create_product(product: Product) -> Product:
    connection = get_db_connection()
    connection.execute("INSERT INTO products ( name, price, stock, description) VALUES (?, ?, ?, ?)",
                       ( product.name, product.price, product.stock, product.description))

    connection.commit()
    connection.close()

    return {"success": True, "message": "Product created successfully", "product": product}

@app.delete("/products/{product_id}")
def delete_product(product_id: int) -> dict:
    cursor = get_db_connection()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    cursor.close()

    return {"message": f"Product with id {product_id} has been deleted."}

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product) -> dict:  
    cursor = get_db_connection()
    cursor.execute("UPDATE products SET name = ?, price = ?, stock = ?, description = ? WHERE id = ?",
                   (updated_product.name, updated_product.price, updated_product.stock, updated_product.description, product_id))
    cursor.commit()
    cursor.close()

    return {"message": f"Product with id {product_id} has been updated."}


@app.get("/products/{product_id}")
def get_product(product_id: int) -> Product:
    cursor = get_db_connection()
    rows = cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchall()
    cursor.close()

    product: Product|None = None
    if rows:
        row = rows[0]
        product = Product(id=row[0], name=row[1], price=row[2], stock=row[3], description=row[4])

    if product is None:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found.")
    return product