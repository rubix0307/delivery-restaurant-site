from flask import Blueprint, render_template, request, redirect

from config import MAX_ORDER_QUANTITY
from functions.db import db_session, OrderDish
from functions.decorators import login_required
from functions.other import get_user_cart_orders

cart = Blueprint('cart', __name__, template_folder='templates')


@cart.route('/', methods=['GET', 'POST'])
@login_required()
def cart_index():
    user, cart, order = get_user_cart_orders()

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
            return redirect(request.referrer)

    context = dict(
        order=order,
    )
    return render_template('cart/cart.html', **context)


@cart.route('/order', methods=['POST'])
@login_required()
def cart_order():
    # Обновить статус заказа
    return