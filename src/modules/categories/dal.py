from sqlmodel import Session, select
from src.db.schemas import Category
from src.db.setup import engine

def get_all():
  with Session(engine) as session:
    return session.exec(select(Category)).all()