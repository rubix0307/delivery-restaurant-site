from flask import Blueprint, render_template

from functions.decorators import login_required


cart = Blueprint('cart', __name__)


@cart.route('/', methods=['GET', 'PUT'])
@login_required()
def cart_index():
    return render_template('base.html')


@cart.route('/order', methods=['POST'])
@login_required()
def cart_order():
    return


@cart.route('/add', methods=['POST'])
@login_required()
def cart_add():
    return