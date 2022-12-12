import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_DRIVER = "sqlite:///instance/shop.db"


def init_test_app():
    app = Flask(__name__)
    app.config['SALT'] = "gskoegi"
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shoptest.db"
    # Dynamically bind SQLAlchemy to application
    db.init_app(app)
    app.app_context().push()  # this does the binding
    return app


def init_app():
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object('src.config.Config')

    db.init_app(app)

    with app.app_context():

        from src.models.user import User
        from src.models.product import Product
        from src.models.order import Order

    #
    #   DROP TABLES
    #

        # Order.drop(SQLALCHEMY_DRIVER)
        # User.drop(SQLALCHEMY_DRIVER)

    #
    #   CREATE ALL TABLES
    #

        db.create_all()

    #
    #   CREATE TABLES
    #

        # User.create("admin","admin@admin.pl","admin",True)

    #
    #
    #

    from src.routes.user import bp as user_bp
    app.register_blueprint(user_bp)

    from src.routes.product import bp as product_bp
    app.register_blueprint(product_bp)

    from src.routes.order import bp as order_bp
    app.register_blueprint(order_bp)

    return app
