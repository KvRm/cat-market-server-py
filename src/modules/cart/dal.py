from sqlmodel import select, Session, and_

from src.db.schemas import Cart, CartsToProducts, Product
from src.db.setup import engine

def get_one(user_id: int):
    with Session(engine) as session:
        return session.exec(select(Cart).where(Cart.user_id == user_id)).first()


def create_cart(user_id: int):
    new_cart = Cart(user_id=user_id)
    with Session(engine) as session:
        session.add(new_cart)
        session.commit()
        session.refresh(new_cart)
        return new_cart


def get_one_with_products(user_id: int):
    result = {
        "cart_id": None,
        "products": [],
    }
    products = {}

    with Session(engine) as session:
        query_result = session.exec(
            select(CartsToProducts)
            .join(Cart)
            .where(Cart.user_id == user_id)
        ).all()

        if not query_result[0]:
            return None

        result['cart_id'] = query_result[0].cart_id

        for cart_to_product in query_result:
            products[cart_to_product.product_id] = {"count": cart_to_product.count}

        pQuery = session.exec(select(Product).where(Product.id.in_(products))).all()

        for p in pQuery:
            result['products'].append({"count": products[p.id]['count'], "id": p.id, "name": p.name, "price": p.price, "image_url": p.image_url})
        
    return result


def clear_cart(user_id: int):
    carts_to_products = get_one(user_id)
    if not carts_to_products:
        return False

    with Session(engine) as session:
        carts_to_products = session.exec(select(CartsToProducts).where(CartsToProducts.cart_id == carts_to_products.id)).all()
        for ctp in carts_to_products:
          session.delete(ctp)
        session.commit()
    return True


def add_product(user_id: int, product_id: int, count: int):
    print(user_id)
    print(user_id)
    print(user_id)
    print(user_id)
    print(user_id)
    cart = get_one(user_id)
    if not cart:
        cart = create_cart(user_id)

    with Session(engine) as session:
        existing_product = session.exec(
            select(CartsToProducts).where(and_(CartsToProducts.cart_id == cart.id, CartsToProducts.product_id == product_id))
        ).first()

        if existing_product:
            if count > 0:
                existing_product.count = count
                session.add(existing_product)
            else:
                session.delete(existing_product)
        else:
            new_cart_to_product = CartsToProducts(cart_id=cart.id, product_id=product_id, count=count)
            session.add(new_cart_to_product)

        session.commit()
    
    return True
