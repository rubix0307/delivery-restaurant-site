import json
from sqlalchemy.engine.row import Row
from flask import session

from functions.db import *


def get_session_user_data():
    return json.loads(session['user'])

def get_user_cart_orders():
    user = get_session_user_data()
    cart = get_or_create(Order, dict(user_id=user['id'], status_id=1))
    orders: Row = db.session.query(Dish, OrderDish.quantity).join(OrderDish).filter(OrderDish.order_id == cart.id).all()
    return user, cart, orders