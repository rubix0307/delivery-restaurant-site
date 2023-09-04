from datetime import datetime, date
from sqlalchemy import func, distinct
from functions.db import Dish, User, Order, OrderDish, db_session


def get_stats(day=date.today()):

    cart_status_id = 1
    check_day = datetime.combine(day, datetime.min.time())

    total_dishes_ordered = (
        db_session.query(Dish, func.sum(OrderDish.quantity).label('total_quantity'))
        .join(OrderDish, Dish.id == OrderDish.dish_id)
        .join(Order, OrderDish.order_id == Order.id)
        .filter(Order.timestamp >= check_day)
        .filter(Order.status_id != cart_status_id)
        .group_by(Dish.name)
        .order_by(func.sum(OrderDish.quantity).desc())
        .all()
    )

    order_stats = (
        db_session.query(
            func.count(Order.id).label('total_orders'),
            func.avg(Order.price).label('average_order_price')
        )
        .filter(Order.timestamp >= check_day)
        .filter(Order.status_id != cart_status_id)
        .first()
    )

    basket_count = (
        db_session.query(func.count(Order.id).label('count'))
        .filter(Order.timestamp >= check_day)
        .filter(Order.status_id == cart_status_id)
        .first()
    )

    users_count = (
        db_session.query(func.count(User.id).label('count'))
        .filter(User.timestamp >= check_day)
        .first()
    )

    registered_and_ordered_users_count = (
        db_session.query(distinct(func.count(User.id).label('count')))
        .join(Order, User.id == Order.user_id)
        .filter(User.timestamp >= check_day)
        .filter(Order.status_id != cart_status_id)
        .first()
    )

    return dict(
        total_dishes_ordered=total_dishes_ordered,
        order_stats=order_stats,
        basket_count=basket_count,
        users_count=users_count,
        registered_and_ordered_users_count=registered_and_ordered_users_count,
    )
