from sqlmodel import Session, select
from src.db.schemas import Product
from src.db.setup import engine

def get_all(search: str = None, categories: list[int] = None):
  with Session(engine) as session:
    statement = select(Product)

    if search:
        statement = statement.where(Product.name.like(f'%{search}%'))

    if categories:
        statement = statement.where(Product.category_id.in_(categories))

    return session.exec(statement).all()