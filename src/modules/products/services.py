from src.modules.products import dal
from typing import List
from fastapi import Query

def get_all_products(categories: List[int] = Query(None), search: str = None):
  return dal.get_all(search, categories)