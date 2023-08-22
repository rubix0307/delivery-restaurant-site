import json
import re

from flask import Blueprint, render_template, session, redirect, url_for, flash, request

from functions.decorators import login_required, logout_required
from functions.db import UserAddress, User, Order, db_session
from functions.edit_text import BcryptPasswordManager

user = Blueprint('user', __name__)


@user.route('/', methods=['GET', 'PUT', 'DELETE'])
@login_required()
def user_index():
    user = session.get('user')
    contex = dict(
        title='Твой аккаунт',
        hide_account_menu=1,
        user=User.query.filter_by(id=user['id']).first()
    )
    return render_template('user_index.html', **contex)


@user.route('/register', methods=['GET','POST'])
@logout_required()
def user_register():
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
        db_session.add(new_user)
        db_session.commit()

        flash('Вы успешно зарегистрированы', 'success')
        return render_template('login.html', **context)

    return render_template('register.html', **context)


@user.route('/login', methods=['GET','POST'])
@logout_required()
def user_login():
    context = dict(
        title='Вход в аккаунт',
        hide_account_menu=1,
        next=request.args.get('next'),
    )

    if request.method == 'POST':
        phone = re.sub(r'\D', '', request.form.get('phone',''))
        password1 = request.form.get('password1')
        context.update(dict(phone=phone))

        search_user = User.query.filter_by(phone=phone).first()
        if search_user:
            if BcryptPasswordManager(password1, search_user.salt, search_user.password).password_check():

                session['user'] = dict(
                    id=search_user.id,
                    name=search_user.name,
                    phone=search_user.phone,
                    email=search_user.email,
                    telegram_id=search_user.telegram_id,
                    role_id=search_user.role_id,
                )
                if context.get('next'):
                    return redirect(context['next'])
                return redirect(url_for('.user_login'))
            flash('Введенный пароль не является корректным', 'error')
        else:
            flash('Пользователь с таким номером телефона не существует', 'error')

    return render_template('login.html', **context)


@user.route('/logout', methods=['GET'])
@login_required()
def user_logout():
    del session['user']
    return redirect(url_for('menu.menu_index'))


@user.route('/restore', methods=['GET', 'POST'])
def user_restore():
    context = dict(
        title='Восстановление пароля',
        hide_account_menu=1,
    )

    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            # email logic ...
            flash('Мы отправили письмо на вашу почту', 'success')
        else:
            flash('Почта должна быть указана', 'error')

    return render_template('user_restore.html', **context)


@user.route('/orders', methods=['GET'])
@login_required()
def user_orders():
    context = dict(
        title='Твои заказы',
        orders=Order.query.filter_by(user_id=session['user'].get('id')).order_by('id').all()
    )

    return render_template('base.html', **context)


@user.route('/orders/<order_id>', methods=['GET'])
@login_required()
def user_order_id(order_id):
    context = dict(
        title='Твой заказ',
        order=Order.query.filter_by(id=order_id, user_id=session['user'].get('id')).first()
    )

    return render_template('base.html', **context)


@user.route('/address', methods=['GET', 'POST'])
@login_required()
def user_address_list():
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
                user_id=session['user'].get('id'),
            )
            db_session.add(new_address)
            db_session.commit()
        else:
            flash('Вы ввели не все обязательные поля', 'error')
            context.update(**request.form)

    context.update(dict(
        user_address_list=UserAddress.query.filter_by(user_id=session['user'].get('id')).all()
    ))

    return render_template('user_address_list.html', **context)


@user.route('/address/<address_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required()
def user_address(address_id):
    context = dict(
        title='Твой адрес',
        address=UserAddress.query.filter_by(id=address_id, user_id=session['user'].get('id')).first()
    )

    return render_template('base.html', **context)