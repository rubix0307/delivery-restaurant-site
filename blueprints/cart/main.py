import time
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import func

from config import MAX_ORDER_QUANTITY
from functions.db import db_session, OrderDish, UserAddress, Dish, Category, Order
from functions.decorators import login_required
from functions.other import get_user_cart_orders
from functions.send_email import SendEmail

cart = Blueprint('cart', __name__, template_folder='templates')


@cart.route('/', methods=['GET', 'POST'])
@login_required()
def cart_index():
    user, cart, order, order_total = get_user_cart_orders()

    if request.method == 'POST':
        dish_id = request.args.get('product_id')
        action = request.args.get('action', '').lower()

        if all([user, cart, dish_id, action]):
            existing_order_dish = db_session.query(OrderDish).filter(
                OrderDish.order_id == cart.id,
                OrderDish.dish_id == dish_id,
                OrderDish.user_id == user['id'],
            ).first()

            if existing_order_dish:
                if action == 'add':
                    if existing_order_dish.quantity < MAX_ORDER_QUANTITY:
                        existing_order_dish.quantity += 1

                elif action == 'remove':
                    if existing_order_dish.quantity > 1:
                        existing_order_dish.quantity -= 1
                    else:
                        db_session.delete(existing_order_dish)

                elif action == 'delete':
                    db_session.delete(existing_order_dish)
            else:
                if action == 'add':
                    db_session.add(OrderDish(
                        order_id=cart.id,
                        dish_id=dish_id,
                        quantity=1,
                        user_id=user['id'],
                    ))

            db_session.commit()
            return redirect(request.referrer) # in next updates add ajax

    context = dict(
        cart=cart,
        order=order,
        user_address_list=UserAddress.query.filter_by(user_id=user.get('id')).all(),
    )
    return render_template('cart/cart.html', **context)


@cart.route('/order', methods=['POST'])
@login_required()
def cart_order():
    user, cart, order, order_total = get_user_cart_orders()
    address = UserAddress.query.filter_by(id=request.form.get('address_id')).first()

    cart.status_id = 2
    cart.address_id = address.id
    cart.price = order_total.price
    cart.calories = order_total.calories
    cart.protein = order_total.protein
    cart.fat = order_total.fat
    cart.carbohydrates = order_total.carbohydrates
    cart.comment = request.form.get('comment','')
    cart.timestamp = datetime.fromtimestamp(time.time())

    db_session.commit()

    email_data = dict(
        subject='Заказ принят | Вилки-Палки',
        receiver_email=user.get('email'),
        message_html=render_template('update_order_status.html', cart=cart, order=order, order_total=order_total, address=address),
    )

    with SendEmail(**email_data) as email:
        is_send = email.send()

    return redirect(url_for('menu.menu_index')) # update: redirect to order