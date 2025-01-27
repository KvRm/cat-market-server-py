from sqlmodel import Session, select
from src.db.schemas import User
from src.db.setup import engine

def get_one(id: int):
  with Session(engine) as session:
    user = session.get(User, id)
    return user

def get_by_email(login: str):
  with Session(engine) as session:
    user = session.exec(select(User).where(User.email == login)).first()
    return user

def update_one(payload: User):
  with Session(engine) as session:
    user = get_one(payload.id)
    if (not user): return False

    user.first_name = payload.first_name
    user.second_name = payload.second_name
    user.last_name = payload.last_name
    user.email = payload.email
    user.phone = payload.phone
    user.sex = payload.sex
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return True

def create_one(payload: User):
  with Session(engine) as session:
    session.add(payload)
    session.commit()
    session.refresh(payload)
    return True