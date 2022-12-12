from flask import Blueprint, make_response, render_template, request, session
from src.models.order import Order
import os
from src.models.security.jwt import token_required

from src.models.user import User

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


@bp.route("/order", methods=["GET"])
@token_required
def api_product_get_by_user_id():
    id = User.get_id_by_email(session['email'])
    orders = Order.get_by_user_id(id)
    if request.method == "GET":
        return render_template("order.html", user_id=id, orders=orders, len=len(orders))


@bp.route("/api/order/create", methods=["POST", "GET"])
@token_required
def api_order_create():
    if request.method == "GET":
        return make_response("aaa")
    user_id = User.get_id_by_email(session['email'])
    products_ids = request.get_json()['products_ids']
    quantities = request.get_json()['quantities']
    print(products_ids)
    print(quantities)
    order = Order.create(user_id, products_ids, quantities, False)
    return order


@bp.route("/api/order/delete", methods=["DELETE"])
def api_order_delete():
    return Order.delete_all()


# @bp.route(API_ORDER_DELETE+"/<int:id>", methods=["DELETE"])
# def api_product_delete_by_id(id=None):
#     if id is not None:
#         return Order.delete_by_id(id)
