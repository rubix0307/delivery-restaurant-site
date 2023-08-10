import json
import re
from flask import Flask, render_template, request, session, redirect, flash, url_for
from sqlalchemy import text
import inspect
import config
from modules.db import *
from modules.edit_text import get_normal_form, BcryptPasswordManager


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

default_time_values = {
    'name': 'Артем',
    'phone': '380660000000',
    'email': 'miroshnichenkoartem0307@gmail.com',
    'password1': '123456',
    'password2': '123456',
}

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
    if not session.get('user'):
        return redirect(url_for('user_sign_in'))

    contex = dict(
        title='Твой аккаунт',
        hide_account_menu=1,
        user=User.query.filter_by(id=session.get('user')).first()
    )
    return render_template('user.html', **contex)


@app.route('/user/register', methods=['GET','POST'])
def user_register():
    if session.get('user'):
        return redirect(url_for('user'))

    context = dict(
        title='Регистрация на сайте',
        hide_account_menu=1,
    )

    if request.method == 'POST':

        name = request.form.get('name')
        email = request.form.get('email')
        phone = re.sub(r'\D', '', request.form.get('phone',''))
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        context.update(dict(**request.form))
        context.update(dict(password1='', password2=''))

        if not all([name, email, phone, password1, password2]):
            flash('Заполнены не все поля', 'error')
            return render_template('register.html', **context)

        if password1 != password2:
            flash('Пароли не совпадают', 'error')
            return render_template('register.html', **context)

        existing_user = User.query.filter_by(phone=phone).first()
        if existing_user:
            flash('Пользователь с таким номером телефона уже существует', 'error')
            return render_template('register.html', **context)

        salt, hashed_password = BcryptPasswordManager(password1).hash_password()
        new_user = User(
            name=name,
            phone=phone,
            email=email,
            salt=salt,
            password=hashed_password,
            role_id=1,
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Вы успешно зарегистрированы', 'success')
        return render_template('sing-in.html', **context)

    return render_template('register.html', **context)


@app.route('/user/sign_in', methods=['GET','POST'])
def user_sign_in():
    if session.get('user'):
        return redirect(url_for('user'))

    context = dict(
        title='Вход в аккаунт',
        hide_account_menu=1,
    )

    if request.method == 'POST':
        phone = re.sub(r'\D', '', request.form.get('phone',''))
        password1 = request.form.get('password1')
        context.update(dict(phone=phone))

        existing_user = User.query.filter_by(phone=phone).first()
        if existing_user:
            if BcryptPasswordManager(password1, existing_user.salt, existing_user.password).password_check():
                session['user'] = existing_user.id
                return redirect(url_for('user'))
            flash('Введенный пароль не является корректным', 'error')
        else:
            flash('Пользователь с таким номером телефона не существует', 'error')

    return render_template('sing-in.html', **context)


@app.route('/user/logout', methods=['GET'])
def user_logout():
    del session['user']
    return redirect(url_for('menu'))


@app.route('/user/restore', methods=['GET', 'POST'])
def user_restore():
    context = dict(
        title='Восстановление пароля',
    )

    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            # email logic ...
            flash('Мы отправили письмо на вашу почту', 'success')
        else:
            flash('Почта должна быть указана', 'error')

    return render_template('user_restore.html', **context)


@app.route('/user/orders', methods=['GET'])
def user_orders():
    if not session.get('user'):
        return redirect(url_for('user_sign_in'))

    context = dict(
        title='Твои заказы',
        orders=Order.query.filter_by(user_id=session.get('user')).order_by('id').all()
    )

    return render_template('base.html', **context)


@app.route('/user/orders/<order_id>', methods=['GET'])
def user_order_id(order_id):
    if not session.get('user'):
        return redirect(url_for('user_sign_in'))

    context = dict(
        title='Твой заказ',
        order=Order.query.filter_by(id=order_id, user_id=session.get('user')).first()
    )

    return render_template('base.html', **context)



@app.route('/user/address', methods=['GET', 'POST'])
def user_address_list():
    if not session.get('user'):
        return redirect(url_for('user_sign_in'))

    context = dict(
        title='Твои адреса',
    )

    if request.method == 'POST':
        city = request.form.get('city')
        street = request.form.get('street')
        house = request.form.get('house')
        apartment = request.form.get('apartment', 0)
        entrance = request.form.get('entrance', 0)
        floor = request.form.get('floor', 0)

        if city and street and house:
            new_address = UserAddress(
                city=city,
                street=street,
                house=house,
                apartment=apartment,
                entrance=entrance,
                floor=floor,
                user_id=session.get('user'),
            )
            db.session.add(new_address)
            db.session.commit()
        else:
            flash('Вы ввели не все обязательные поля', 'error')
            context.update(**request.form)

    context.update(dict(
        user_address_list=UserAddress.query.filter_by(user_id=session.get('user')).all()
    ))

    return render_template('user_address_list.html', **context)


@app.route('/user/address/<address_id>', methods=['GET', 'PUT', 'DELETE'])
def user_address(address_id):
    if not session.get('user'):
        return redirect(url_for('user_sign_in'))

    context = dict(
        title='Твой адрес',
        addess=UserAddress.query.filter_by(id=address_id, user_id=session.get('user')).first()
    )

    return render_template('base.html', **context)

@app.route('/', methods=['GET'])
@app.route('/menu', methods=['GET'])
def menu():
    context = dict(
        categories=Category.query.all(),
        products=db.session.query(Dish, Category).join(Category).order_by('category_id').all(),
    )

    return render_template('menu.html', **context)


@app.route('/menu/<category_slug>', methods=['GET'])
def menu_category(category_slug):
    products = db.session.query(Dish, Category).join(Category).filter(Category.slug == category_slug).order_by('category_id').all()
    context = dict(
        categories=Category.query.all(),
        products=products,
    )

    return render_template('menu.html', **context)


@app.route('/menu/<category_slug>/<dish_slug>', methods=['GET', 'POST'])
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


@app.route('/menu/search', methods=['GET'])
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
    app.run(host='0.0.0.0', debug=True)
