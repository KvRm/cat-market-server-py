from fastapi import HTTPException
from src.db.schemas import User
from src.modules.user import dal

def get_user_by_email(email: str):
  user = dal.get_by_email(email)
  if (not user): raise HTTPException(status_code=404, detail="User not found")
  return user

def update_user(user: User):
  is_success = dal.update_one(user)
  if (not is_success): raise HTTPException(status_code=500, detail="Failed to update user")
  return is_success

def create_user(user: User):
  is_success = dal.create_one(user)
  if (not is_success): raise HTTPException(status_code=500, detail="Failed to create user")
  return is_success