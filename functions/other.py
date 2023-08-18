import json

from flask import session

from functions.db import *


def get_session_user_data():
    return json.loads(session['user'])

def get_user_cart_orders():
    user = get_session_user_data()
    cart = get_or_create(Order, dict(user_id=user['id'], status_id=1))

    try:
        orders: (Dish, OrderDish.quantity) = db.session.query(Dish, OrderDish.quantity).join(OrderDish).filter(OrderDish.order_id == cart.id).all()
    except Exception as ex:
        print(ex)
    return user, cart, orders