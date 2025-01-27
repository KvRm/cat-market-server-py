from fastapi import FastAPI

from src.modules.auth import services

def setup_auth_module(app: FastAPI):
  app.post("/auth/register")(services.register)
  app.post("/auth/login")(services.login)
