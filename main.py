from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.db.setup import create_db_and_tables
from src.modules.auth.setup import setup_auth_module
from src.modules.cart.setup import setup_carts_module
from src.modules.categories.setup import setup_categories_module
from src.modules.products.setup import setup_products_module
from src.modules.user.setup import setup_users_module
from src.scripts.set_db_initial_data import set_db_initial_data

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/public", StaticFiles(directory="public"), name="public")

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()
    set_db_initial_data()

setup_auth_module(app)
setup_users_module(app)
setup_products_module(app)
setup_categories_module(app)
setup_carts_module(app)