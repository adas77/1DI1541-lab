import sqlalchemy
from src import init_app
from src.models.order import order_product, Order


def drop():
    app = init_app()
    with app.app_context():
        Order.__table__.drop()
        order_product.__table__.drop()


if __name__ == "__main__":
    engine = sqlalchemy.create_engine('sqlite:///instance/shop.db')
    Order.drop(engine)
