from flask import Flask, render_template, request
from sqlalchemy import text
import config
from modules.db import *
from modules.edit_text import get_normal_form

app = Flask(__name__)
app.config.update(dict(
        debug=config.DEBUG,
        SECRET_KEY=config.SECRET_KEY,
        SQLALCHEMY_DATABASE_URI=config.SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER='uploads',
    ))

db.init_app(app)

with app.app_context():
    db.create_all()
    db.session.commit()
    dishes = Dish.query.all()


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.route('/cart', methods=['GET', 'PUT'])
def cart():
    return render_template('base.html')


@app.route('/cart/order', methods=['POST'])
def cart_order():
    return


@app.route('/cart/add', methods=['POST'])
def cart_add():
    return


@app.route('/user', methods=['GET', 'PUT', 'DELETE'])
def user():
    return render_template('base.html')


@app.route('/user/register', methods=['GET','POST'])
def user_register():
    context = {
        'title': 'Регистрация на сайте',
        'hide_account_menu': True,
    }
    return render_template('register.html', **context)


@app.route('/user/sign_in', methods=['GET','POST'])
def user_sign_in():
    context = {
        'title': 'Вход в аккаунт',
        'hide_account_menu': True,
    }
    return render_template('sing-in.html', **context)


@app.route('/user/logout', methods=['POST'])
def user_logout():
    return


@app.route('/user/restore', methods=['POST'])
def user_restore():
    return


@app.route('/user/orders', methods=['GET'])
def user_orders():
    return render_template('base.html')


@app.route('/user/orders/<order_id>', methods=['GET'])
def user_order_id(order_id):
    return render_template('base.html')


@app.route('/user/address', methods=['GET', 'POST'])
def user_address_list():
    return render_template('base.html')


@app.route('/user/address/<address_id>', methods=['GET', 'PUT', 'DELETE'])
def user_address(address_id):
    return render_template('base.html')

@app.route('/', methods=['GET'])
@app.route('/menu', methods=['GET'])
def menu():
    context = dict(
        categories=Category.query.all(),
        products=Dish.query.order_by('category_id').all(),
    )

    return render_template('menu.html', **context)


@app.route('/menu/<category_slug>', methods=['GET'])
def menu_category(category_slug):
    category = Category.query.filter_by(slug=category_slug).first()
    products = Dish.query.filter_by(category_id=category.id).all()

    context = dict(
        categories=Category.query.all(),
        products=products,
    )

    return render_template('menu.html', **context)


@app.route('/menu/<category_slug>/<dish_slug>', methods=['GET'])
def menu_dish(category_slug, dish_slug):
    product = Dish.query.filter_by(category_id=category_slug, slug=dish_slug).first()
    context = dict(
        categories=Category.query.all(),
        product=product,
    )
    return render_template('product.html', **context)


@app.route('/menu/<category_slug>/<dish_slug>/review', methods=['POST'])
def menu_review(category_slug, dish_slug):
    return


@app.route('/menu/search', methods=['GET'])
def menu_search():
    search_query = request.args.get('search_query', '').strip()
    search_query_normal = get_normal_form(search_query)

    print(f'{search_query=}\n{search_query_normal=}')

    products = Dish.query.filter(text('name_normal LIKE :search_query_normal')).params(search_query_normal=f'%{search_query_normal}%').all()
    context = dict(
        categories=Category.query.all(),
        products=products,
        search_query=search_query,
    )

    return render_template('menu.html', **context)


@app.route('/admin', methods=['GET'])
def admin():
    return render_template('base.html')

@app.route('/admin/dishes', methods=['GET', 'POST'])
def admin_dishes():
    return render_template('base.html')

@app.route('/admin/dishes/<dish>', methods=['GET', 'PUT', 'DELETE'])
def admin_dish(dish):
    return render_template('base.html')

@app.route('/admin/categories', methods=['GET', 'POST'])
def admin_categories():
    return render_template('base.html')

@app.route('/admin/categories/<category>', methods=['GET', 'PUT', 'DELETE'])
def admin_category(category):
    return render_template('base.html')

@app.route('/admin/orders', methods=['GET'])
def admin_orders():
    return render_template('base.html')

@app.route('/admin/orders/<order>', methods=['GET', 'PUT'])
def admin_order(order):
    return render_template('base.html')

@app.route('/admin/search', methods=['GET'])
def admin_search():
    return render_template('base.html')


if __name__ == '__main__':
    print(123)
    app.run(host='0.0.0.0', debug=True)
