import datetime
from pydantic._internal._generate_schema import GenerateSchema
from pydantic_core import core_schema
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, SQLModel

# ---- https://github.com/pydantic/pydantic/discussions/9343#discussioncomment-10723743
initial_match_type = GenerateSchema.match_type
def match_type(self, obj):
    if getattr(obj, "__name__", None) == "datetime":
        return core_schema.datetime_schema()
    return initial_match_type(self, obj)
GenerateSchema.match_type = match_type
# ----

class CartsToProducts(SQLModel, table=True):
    cart_id: int = Field(nullable=False, foreign_key="cart.id", primary_key=True)
    product_id: int = Field(nullable=False, foreign_key="product.id", primary_key=True)
    count: int = Field(nullable=False)

class Cart(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)

    user_id: int = Field(foreign_key="user.id", nullable=False)
    user: "User" = Relationship(back_populates="cart")
    products: list["Product"] = Relationship(back_populates="carts", link_model=CartsToProducts)

    updated_at: datetime = Field(sa_column=Column(DateTime, default=func.now(), onupdate=func.now()))
    created_at: datetime = Field(sa_column=Column(DateTime, default=func.now()))

class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(nullable=False, max_length=256)

    products: list["Product"] = Relationship(back_populates="category")

    updated_at: datetime = Field(sa_column=Column(DateTime, default=func.now(), onupdate=func.now()))
    created_at: datetime = Field(sa_column=Column(DateTime, default=func.now()))


class Product(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(nullable=False, max_length=256)
    image_url: str = Field(nullable=False, max_length=1024)
    price: int = Field(nullable=False)

    category_id: int = Field(foreign_key="category.id", nullable=False)
    category: Category = Relationship(back_populates="products")
    carts: list[Cart] = Relationship(back_populates="products", link_model=CartsToProducts)

    updated_at: datetime = Field(sa_column=Column(DateTime, default=func.now(), onupdate=func.now()))
    created_at: datetime = Field(sa_column=Column(DateTime, default=func.now()))


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    first_name: str = Field(nullable=False, max_length=256)
    second_name: str = Field(max_length=256)
    last_name: str = Field(nullable=False, max_length=256)
    email: str = Field(nullable=False, max_length=256, unique=True, index=True)
    phone: str = Field(nullable=False, max_length=20, unique=True, index=True)
    sex: int = Field(nullable=False)
    password: str = Field(nullable=False)

    cart: Cart = Relationship(back_populates="user")
    
    updated_at: datetime = Field(sa_column=Column(DateTime, default=func.now(), onupdate=func.now()))
    created_at: datetime = Field(sa_column=Column(DateTime, default=func.now()))