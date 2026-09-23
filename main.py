from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlmodel import select
from src.models.product_model import Product
from src.shared.database.session_db import SessionDep, get_session

app = FastAPI()

class CreateProduct(BaseModel):
    name: str
    price: float
    quantity: int
    category: str


@app.post("/product")
def create_product(product: CreateProduct, session: SessionDep):
    product = Product(name = product.name, category= product.category, price=product.price, quantity=product.quantity)
    session.add(product)
    session.commit()
    session.refresh(product)

    return product

@app.get("/product")
def get_products(session: SessionDep):
    products = session.exec(
        select(Product)
    ).all()

    return products

@app.delete('/product/{id}')
def delete_product(product_id: int, session: SessionDep):
    product = session.exec(
            select(Product).where(Product.id == product_id)
    ).one()
    session.delete(product)
    session.commit()