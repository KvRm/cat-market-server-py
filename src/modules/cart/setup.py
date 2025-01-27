from fastapi import FastAPI

from src.modules.cart import services

def setup_carts_module(app: FastAPI):
  app.get("/carts/current")(services.get_current)
  app.post("/carts/add-product")(services.add_product)
  app.post("/carts/clear")(services.clear)
