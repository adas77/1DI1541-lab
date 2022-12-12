from flask import Blueprint, jsonify, render_template, request, url_for
from src.models.product import Product
from ..models.security.jwt import handle_login, token_required,is_admin
import os

API_PRODUCT_GET = os.getenv('API_PRODUCT_GET')
API_PRODUCT_CREATE = os.getenv('API_PRODUCT_CREATE')
API_PRODUCT_UPDATE = os.getenv('API_PRODUCT_UPDATE')
API_PRODUCT_DELETE = os.getenv('API_PRODUCT_DELETE')

bp = Blueprint('product', __name__)


@bp.route('/product')
@token_required
def product():
    if is_admin():
        return render_template('admin/super_product.html')
    else:
        return render_template('product.html')


@bp.route(API_PRODUCT_GET, methods=["GET"])
@token_required
def api_product_get():
    products = Product.get_products()
    return products


@bp.route(API_PRODUCT_GET+"/<int:id>", methods=["GET"])
@token_required
def api_product_get_by_id(id=None):
    if id is not None:
        product = Product.get_by_id(id)
        img = product['img']
        img_url = url_for('static', filename=f'img/{img}')
        return render_template("product_detail.html", id=product['product_id'], img=img, img_url=img_url, description=product['description'], price=product['price'], quantity=product['quantity'], date=product['reg_date'])


@bp.route(API_PRODUCT_CREATE, methods=["POST", "GET"])
@token_required
def api_product_create():
    if request.method == "GET":
        return render_template("admin/super_product.html")
    img = request.form['img']
    price = request.form['price']
    description = request.form['description']
    quantity = request.form['quantity']
    product = Product.create(img, price, quantity, description)
    return product

@bp.route(API_PRODUCT_UPDATE+"/<int:id>", methods=["POST"])
@token_required
def api_product_update(id=None):
    if id is not None:
        discount = request.get_json()['discount']
        product = Product.update(id,discount)
        return product

@bp.route(API_PRODUCT_DELETE, methods=["DELETE"])
@token_required
def api_product_delete():
    return Product.delete_all()


@bp.route(API_PRODUCT_DELETE+"/<int:id>", methods=["DELETE"])
@token_required
def api_product_delete_by_id(id=None):
    if id is not None:
        return Product.delete_by_id(id)
