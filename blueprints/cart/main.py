from flask import Blueprint, render_template

from functions import decorators as d


cart = Blueprint('cart', __name__)


@cart.route('/', methods=['GET', 'PUT'])
@d.login_required()
def cart_index():
    return render_template('base.html')


@cart.route('/order', methods=['POST'])
@d.login_required()
def cart_order():
    return


@cart.route('/add', methods=['POST'])
@d.login_required()
def cart_add():
    return