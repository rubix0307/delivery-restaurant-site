from sqlalchemy import text
from flask import Blueprint, render_template, request

from functions.db import db, Category, Dish
from functions.edit_text import get_normal_form


menu = Blueprint('menu', __name__)


@menu.route('/', methods=['GET'])
def menu_index():
    context = dict(
        categories=Category.query.all(),
        products=db.session.query(Dish, Category).join(Category).order_by('category_id').all(),
    )

    return render_template('menu.html', **context)


@menu.route('/menu/<category_slug>', methods=['GET'])
def menu_category(category_slug):
    products = db.session.query(Dish, Category).join(Category).filter(Category.slug == category_slug).order_by('category_id').all()
    context = dict(
        categories=Category.query.all(),
        products=products,
    )

    return render_template('menu.html', **context)


@menu.route('/menu/<category_slug>/<dish_slug>', methods=['GET', 'POST'])
def menu_dish(category_slug, dish_slug):
    product = db.session.query(Dish).join(Category).filter(Category.slug == category_slug, Dish.slug == dish_slug).first()
    context = dict(
        categories=Category.query.all(),
        product=product,
    )

    if request.method == 'POST':

        product.name = request.form.get('name', product.name)
        product.name_normal = get_normal_form(product.name)
        product.slug = request.form.get('slug', product.slug) # and update slug, but there is no slug function ye, product.slugt
        product.price = request.form.get('price', product.price)
        product.description = request.form.get('description', product.description)
        product.category_id = request.form.get('category_id', product.category_id)
        product.available = request.form.get('available', product.available)
        product.photo = request.form.get('photo', product.photo) # save photo and set path
        product.weight = request.form.get('weight', product.weight)
        product.calories = request.form.get('calories', product.calories)
        product.protein = request.form.get('protein', product.protein)
        product.fat = request.form.get('fat', product.fat)
        product.carbohydrates = request.form.get('carbohydrates', product.carbohydrates)

        db.session.commit()

    return render_template('product.html', **context)


@menu.route('/menu/search', methods=['GET'])
def menu_search():
    search_query = request.args.get('search_query', '').strip()
    search_query_normal = get_normal_form(search_query)

    products = db.session.query(Dish, Category)\
        .join(Category)\
        .filter(text('name_normal LIKE :search_query_normal'))\
        .params(search_query_normal=f'%{search_query_normal}%')\
        .order_by('category_id')\
        .all()

    context = dict(
        categories=Category.query.all(),
        products=products,
        search_query=search_query,
    )

    return render_template('menu.html', **context)