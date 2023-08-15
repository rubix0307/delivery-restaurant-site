from flask import Blueprint, render_template
from functions import decorators as d


admin = Blueprint('admin', __name__)


@admin.route('/', methods=['GET'])
@d.login_required(role_ids=[2,3,4])
def admin_index():
    return render_template('base.html')


@admin.route('/dishes', methods=['GET', 'POST'])
@d.login_required(role_ids=[2,3,4])
def admin_dishes():
    return render_template('base.html')


@admin.route('/dishes/<dish>', methods=['GET', 'PUT', 'DELETE'])
@d.login_required(role_ids=[2])
def admin_dish(dish):
    return render_template('base.html')


@admin.route('/categories', methods=['GET', 'POST'])
@d.login_required(role_ids=[2])
def admin_categories():
    return render_template('base.html')


@admin.route('/categories/<category>', methods=['GET', 'PUT', 'DELETE'])
@d.login_required(role_ids=[2])
def admin_category(category):
    return render_template('base.html')


@admin.route('/orders', methods=['GET'])
@d.login_required(role_ids=[2,4])
def admin_orders():
    return render_template('base.html')


@admin.route('/orders/<order>', methods=['GET', 'PUT'])
@d.login_required(role_ids=[2,4])
def admin_order(order):
    return render_template('base.html')


@admin.route('/search', methods=['GET'])
@d.login_required(role_ids=[2,3,4])
def admin_search():
    return render_template('base.html')