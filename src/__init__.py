from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app():
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object('src.config.Config')

    db.init_app(app)

    with app.app_context():

        from src.models.user import User
        from src.models.product import Product
        db.create_all()

        from src.routes.user import bp as user_bp
        app.register_blueprint(user_bp)
        
        from src.routes.product import bp as product_bp
        app.register_blueprint(product_bp)

        return app
