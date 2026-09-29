
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from db import get_db
from schemas import Product
from routes.auth import auth_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_routes)

@app.get("/products")
def get_products() -> list[Product]:
    connection = get_db()
    rows = connection.execute("SELECT * FROM products").fetchall()

    connection.close()

    product_list = []
    for row in rows:
        product = Product(id=row[0], name=row[1], price=row[2], stock=row[3], description=row[4])
        product_list.append(product)


    return product_list


@app.put("/products/add-to-cart/{id}")
def add_to_cart(id:int):
    connection = get_db()

    row = connection.execute("select * from cart where product_id = ?", (id,)).fetchone()

    if(row is not None):
        raise HTTPException(status_code=400, detail="Item is already in cart")

    row = connection.execute("select * from products where id = ?", (id,)).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Product not found")

    product = Product(**dict(row))
    prev_stock = product.stock

    if prev_stock <= 0:
        raise HTTPException(
                status_code=400,
                detail="This item is out of stock"
        )
    new_stock = prev_stock -  1
    
    connection.execute("update products set stock = ? where id = ?", (new_stock, id))
    updated_product = Product(**dict(row))

    connection.execute("insert into cart values (?)",((updated_product.id,)))

    row = connection.execute("""
                            select 
                                products.id as id,
                                products.stock as stock,
                                products.description as desctiption,
                                products.price as price,
                                products.name as name
                            
                            from cart left join products on cart.product_id=products.id
                            """).fetchall()
    products = list(row)
    connection.commit()
    connection.close()

    return {
        "success": True,
        "message":"added to cart successfully",
        "products":products
    } 
    

