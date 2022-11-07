from flask import Blueprint, make_response, render_template, request
from src.models.order import Order
import os

# API_ORDER_GET = os.getenv('API_ORDER_GET')
# API_ORDER_CREATE = os.getenv('API_ORDER_CREATE')
# API_ORDER_UPDATE = os.getenv('API_ORDER_UPDATE')
# API_ORDER_DELETE = os.getenv('API_ORDER_DELETE')
# API_PRODUCT_DELETE = os.getenv('API_PRODUCT_DELETE')
# print(API_ORDER_GET)
# print(API_ORDER_CREATE)
# print(API_ORDER_UPDATE)
# print(API_ORDER_DELETE)
# print(API_PRODUCT_DELETE)
# todo: fixme

bp = Blueprint('order', __name__)


# @bp.route(API_ORDER_GET, methods=["GET"])
# def api_order_get():
#     products = Order.get_products()
#     return products


# @bp.route(API_ORDER_GET+"/<int:id>", methods=["GET"])
# def api_order_get_by_id(id=None):
#     if id is not None:
#         products = Order.get_by_id(id)
#         return products


@bp.route("/api/order/create", methods=["POST", "GET"])
def api_order_create():
    if request.method == "GET":
        return make_response("aaa")
    print(f'req:{request.get_json()}')
    user_id = request.get_json()['user_id']
    products_ids = request.get_json()['products_ids']
    print(user_id)
    print(products_ids)
    print(type(products_ids))
    order = Order.create(user_id, products_ids)
    return order


@bp.route("/api/order/delete", methods=["DELETE"])
def api_order_delete():
    return Order.delete_all()


# @bp.route(API_ORDER_DELETE+"/<int:id>", methods=["DELETE"])
# def api_product_delete_by_id(id=None):
#     if id is not None:
#         return Order.delete_by_id(id)
