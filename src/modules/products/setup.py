from fastapi import FastAPI

from src.modules.products import services

def setup_products_module(app: FastAPI):
  app.get("/products/all")(services.get_all_products)
