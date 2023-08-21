import json
from functools import wraps
from flask import session, flash, redirect, url_for
from functions.db import User


def login_required(role_ids: list[int] = [], redirect_to:str='user.user_login'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_exists = session.get('user')

            if user_exists and not role_ids:
                return f(*args, **kwargs)

            elif user_exists and role_ids:
                user = User.query.filter_by(id=user_exists.get('id')).one()

                if user and user.role_id in role_ids:
                    return f(*args, **kwargs)
                flash('Недостаточно прав', 'error')
            else:
                flash('Авторизуйтесь для входа на эту страницу', 'error')

            return redirect(url_for(redirect_to))
        return decorated_function
    return decorator

def logout_required(redirect_to='user.user_index'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_exists = session.get('user')

            if not user_exists:
                return f(*args, **kwargs)

            return redirect(url_for(redirect_to))
        return decorated_function
    return decorator