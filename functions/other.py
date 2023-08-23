import json
from sqlalchemy.engine.row import Row
from flask import session

from functions.db import *


def get_user_cart_orders():
    user = session.get('user')
    cart = get_or_create(Order, dict(user_id=user.get('id'), status_id=1))
    orders: Row[Dish, Category, OrderDish] = db_session.query(Dish, Category, OrderDish)\
        .join(OrderDish).filter(OrderDish.order_id == cart.id, OrderDish.user_id == user.get('id'))\
        .join(Category).filter(Dish.category_id == Category.id)\
        .all()
    return user, cart, orders