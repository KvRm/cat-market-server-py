from typing import Annotated
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from src.db.schemas import User
from src.modules.auth.services import get_request_user
from src.modules.cart import dal

class AddProductParams(BaseModel):
    product_id: int
    count: int

def get_current(current_user: Annotated[User, Depends(get_request_user)]):
  cart = dal.get_one_with_products(current_user.id)
  if (not cart): raise HTTPException(404, "Cart not found")
  return cart

def add_product(params: AddProductParams, current_user: Annotated[User, Depends(get_request_user)]):
  is_success = dal.add_product(current_user.id, params.product_id, params.count)
  if (not is_success): raise HTTPException(500, "Failed to add product")
  return True

def clear(current_user: Annotated[User, Depends(get_request_user)]):
  is_success = dal.clear_cart(current_user.id)
  print(current_user.id)
  if (not is_success): raise HTTPException(500, "Failed to clear cart")
  return True
