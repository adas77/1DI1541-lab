from flask import Blueprint, jsonify, render_template, request
from src.models.product import Product
from ..models.security.jwt import handle_login, token_required
import os

API_PRODUCT_GET = os.getenv('API_PRODUCT_GET')
API_PRODUCT_CREATE = os.getenv('API_PRODUCT_CREATE')
API_PRODUCT_UPDATE = os.getenv('API_PRODUCT_UPDATE')
API_PRODUCT_DELETE = os.getenv('API_PRODUCT_DELETE')

bp = Blueprint('product', __name__)


@bp.route(API_PRODUCT_GET, methods=["GET"])
def api_productr_get():
    products = Product.get_products()
    return products


@bp.route(API_PRODUCT_GET+"/<int:id>", methods=["GET"])
def api_product_get_by_id(id=None):
    if id is not None:
        products = Product.get_by_id(id)
        return products


@bp.route(API_PRODUCT_CREATE, methods=["POST", "GET"])
def api_product_create():
    if request.method == "GET":
        return render_template("admin/create_product.html")
    img = request.form['img']
    price = request.form['price']
    description = request.form['description']
    quantity = request.form['quantity']
    product = Product.create(img, price, quantity, description)
    return product


@bp.route(API_PRODUCT_DELETE, methods=["DELETE"])
def api_product_delete():
    return Product.delete_all()


@bp.route(API_PRODUCT_DELETE+"/<int:id>", methods=["DELETE"])
def api_product_delete_by_id(id=None):
    if id is not None:
        return Product.delete_by_id(id)