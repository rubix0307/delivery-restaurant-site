from flask import Blueprint, render_template, request, url_for
from functions.db import Dish, Category, db_session
from functions.decorators import login_required
from functions.edit_text import get_normal_form, create_slug

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/', methods=['GET'])
@login_required(role_ids=[2,3,4])
def admin_index():
    context = dict(
        categories=Category.query.all(),
        products=db_session.query(Dish, Category).join(Category).order_by('category_id').all(),
    )
    return render_template('admin/admin.html', **context)


@admin.route('/dishes', methods=['GET', 'POST'])
@login_required(role_ids=[2,3,4])
def admin_dishes():

    if request.method == 'POST':

        product = Dish()
        product.name = request.form.get('name')
        product.name_normal = get_normal_form(product.name)
        product.slug = create_slug(product.name)
        product.price = request.form.get('price')
        product.description = request.form.get('description')
        product.category_id = request.form.get('category_id')
        product.available = request.form.get('available') == 'on'
        product.photo = request.form.get('photo')  # save photo and set path
        product.weight = request.form.get('weight')
        product.calories = request.form.get('calories')
        product.protein = request.form.get('protein')
        product.fat = request.form.get('fat')
        product.carbohydrates = request.form.get('carbohydrates')

        db_session.add(product)
        db_session.commit()

    context = dict(
        categories=Category.query.all(),
        products=db_session.query(Dish, Category).join(Category).order_by('category_id').all(),
    )

    return render_template('admin/admin.html', **context)

@admin.route('/dishes/<dish>', methods=['GET', 'PUT', 'DELETE'])
@login_required(role_ids=[2])
def admin_dish(dish):
    return render_template('base.html')


@admin.route('/categories', methods=['GET', 'POST'])
@login_required(role_ids=[2])
def admin_categories():
    if request.method == 'POST':
        category = Category()
        category.name = request.form.get('name')
        category.slug = create_slug(category.name)
        category.photo = request.form.get('photo')  # save photo and set path

        db_session.add(category)
        db_session.commit()

    context = dict()
    return render_template('admin/admin.html', **context)


@admin.route('/categories/<category>', methods=['GET', 'PUT', 'DELETE'])
@login_required(role_ids=[2])
def admin_category(category):
    return render_template('base.html')


@admin.route('/orders', methods=['GET'])
@login_required(role_ids=[2,4])
def admin_orders():
    return render_template('base.html')


@admin.route('/orders/<order>', methods=['GET', 'PUT'])
@login_required(role_ids=[2,4])
def admin_order(order):
    return render_template('base.html')


@admin.route('/search', methods=['GET'])
@login_required(role_ids=[2,3,4])
def admin_search():
    return render_template('base.html')