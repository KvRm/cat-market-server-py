from fastapi import FastAPI

from src.modules.categories import services

def setup_categories_module(app: FastAPI):
  app.get("/categories/all")(services.get_all_categories)
