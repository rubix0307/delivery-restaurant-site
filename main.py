from flask import Flask, render_template, request
import config

app = Flask(__name__)
app.config.update(dict(
    DEBUG=config.DEBUG,
    SECRET_KEY=config.SECRET_KEY,
))

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


@app.route('/menu', methods=['GET'])
def menu():
    order_by = request.args.get('order_by', 'name')
    dec = request.args.get('dec', False)
    return render_template('base.html')


@app.route('/menu/<category_name>', methods=['GET'])
def menu_category(category_name):
    order_by = request.args.get('order_by', 'name')
    dec = request.args.get('dec', False)
    return render_template('base.html')


@app.route('/menu/<cat_name>/<dish>', methods=['GET'])
def menu_dish(cat_name, dish):
    return render_template('base.html')


@app.route('/menu/<cat_name>/<dish>/review', methods=['POST'])
def menu_review(cat_name, dish):
    return


@app.route('/menu/search', methods=['POST'])
def menu_search():
    return


if __name__ == '__main__':
    app.run(host='0.0.0.0')
