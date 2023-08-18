from flask import Blueprint, render_template

from functions.decorators import login_required
from functions.other import get_user_cart_orders

cart = Blueprint('cart', __name__, template_folder='templates')


@cart.route('/', methods=['GET', 'PUT'])
@login_required()
def cart_index():
    user, cart, order = get_user_cart_orders()

    context = dict(
        user=user,
        cart=cart,
        order=order,
    )

    return render_template('cart/cart.html', **context)


@cart.route('/order', methods=['POST'])
@login_required()
def cart_order():
    user, cart, order = get_user_cart_orders()



    return


@cart.route('/add', methods=['POST'])
@login_required()
def cart_add():
    user, cart, order = get_user_cart_orders()
    return