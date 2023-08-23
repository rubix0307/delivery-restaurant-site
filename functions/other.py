import json

from sqlalchemy import func
from sqlalchemy.engine.row import Row
from flask import session

from functions.db import *


def get_user_cart_orders():
    user: dict = session.get('user')
    cart: Order = get_or_create(Order, dict(user_id=user.get('id'), status_id=1))

    order: Row[Dish, Category, OrderDish] = db_session.query(Dish, Category, OrderDish)\
        .join(OrderDish).filter(OrderDish.order_id == cart.id, OrderDish.user_id == user.get('id'))\
        .join(Category).filter(Dish.category_id == Category.id)\
        .all()
    order_total = db_session.query(
        func.sum(Dish.price).label("price"),
        func.sum(Dish.weight).label("weight"),
        func.sum(Dish.calories).label("calories"),
        func.sum(Dish.protein).label("protein"),
        func.sum(Dish.fat).label("fat"),
        func.sum(Dish.carbohydrates).label("carbohydrates")
    ).join(OrderDish).filter(OrderDish.order_id == cart.id, OrderDish.user_id == user.get('id')).first()

    return user, cart, order, order_total