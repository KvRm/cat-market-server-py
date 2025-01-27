from sqlmodel import Session, select

from src.db.setup import engine
from src.db.schemas import Category, Product

def set_db_initial_data():
    with Session(engine) as session:
        is_categories_table_empty = not session.get(Category, 1)

        if is_categories_table_empty:
            session.add_all([
                Category(name='Геймпады'),
                Category(name='Мониторы'),
                Category(name='Клавиатуры'),
                Category(name='Ноутбуки'),
            ])
            session.commit()

        is_products_table_empty = not session.get(Product, 1)

        if is_products_table_empty:
            session.add_all([
                Product(id=1, category_id=1, name='Геймпад Sony DualSense', image_url='/public/products/geympad.jpg', price=8299),
                Product(id=2, category_id=2, name='Монитор ASUS TUF Gaming', image_url='/public/products/monitor.jpg', price=16399),
                Product(id=3, category_id=3, name='Клавиатура Logitech K380', image_url='/public/products/keyboard.jpg', price=2599),
                Product(id=4, category_id=4, name='Ноутбук MSI Katana', image_url='/public/products/laptop.jpg', price=65999),
            ])
            session.commit()