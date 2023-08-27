import os

from sqlalchemy import text
from flask import Blueprint, render_template, request, url_for

from functions.db import Category, Dish, db_session
from functions.edit_text import get_normal_form, create_slug
from functions.other import get_user_cart_orders
from functions.send_email import SendEmail
menu = Blueprint('', __name__)


@menu.route('/', methods=['GET'])
def menu_index():
    context = dict(
        categories=Category.query.all(),
        products=db_session.query(Dish, Category).join(Category).order_by('category_id').all(),
    )

    return render_template('menu.html', **context)


@menu.route('/<category_slug>', methods=['GET'])
def menu_category(category_slug):
    products = db_session.query(Dish, Category).join(Category).filter(Category.slug == category_slug).order_by('category_id').all()
    context = dict(
        categories=Category.query.all(),
        products=products,
    )

    return render_template('menu.html', **context)


@menu.route('/<category_slug>/<dish_slug>', methods=['GET', 'POST'])
def menu_dish(category_slug, dish_slug):
    product = db_session.query(Dish, Category).join(Category).filter(Category.slug == category_slug, Dish.slug == dish_slug).first()
    context = dict(
        categories=Category.query.all(),
        product=product,
    )

    if request.method == 'POST':

        product.Dish.name = request.form.get('name', product.Dish.name)
        product.Dish.name_normal = get_normal_form(product.Dish.name)
        product.Dish.slug = create_slug(product.Dish.name)
        product.Dish.price = request.form.get('price', product.Dish.price)
        product.Dish.description = request.form.get('description', product.Dish.description)
        product.Dish.category_id = request.form.get('category_id', product.Dish.category_id)
        product.Dish.available = request.form.get('available', product.Dish.available)
        product.Dish.photo = request.form.get('photo', product.Dish.photo) # save photo and set path
        product.Dish.weight = request.form.get('weight', product.Dish.weight)
        product.Dish.calories = request.form.get('calories', product.Dish.calories)
        product.Dish.protein = request.form.get('protein', product.Dish.protein)
        product.Dish.fat = request.form.get('fat', product.Dish.fat)
        product.Dish.carbohydrates = request.form.get('carbohydrates', product.Dish.carbohydrates)

        db_session.commit()

    return render_template('product.html', **context)


@menu.route('/search', methods=['GET'])
def menu_search():
    search_query = request.args.get('search_query', '').strip()
    search_query_normal = get_normal_form(search_query)

    products = db_session.query(Dish, Category)\
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
