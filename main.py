from flask import Flask, render_template

import config
from blueprints import admin, menu, user, cart


app = Flask(__name__)
app.config.update(config.app_config)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(menu, url_prefix='/menu')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(cart, url_prefix='/cart')


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
