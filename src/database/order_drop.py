import sqlalchemy
# from src import init_app
from src.models.order import order_product, Order


def drop():
    # app = init_app()
    # with app.app_context():
    engine = sqlalchemy.create_engine('sqlite:///instance/shop.db')
    Order.__table__.drop(engine)
    order_product.__table__.drop(engine)


if __name__ == "__main__":
    engine = sqlalchemy.create_engine('sqlite:///instance/shop.db')
    Order.drop(engine)
