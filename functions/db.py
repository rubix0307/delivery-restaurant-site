from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(255))

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_normal = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    available = db.Column(db.Boolean, default=True)
    photo = db.Column(db.String(255))
    weight = db.Column(db.Integer)
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)
    carbohydrates = db.Column(db.Float)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    salt = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    telegram_id = db.Column(db.String(50))
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'), nullable=False, default=1)


class UserAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    house = db.Column(db.String(20), nullable=False)
    apartment = db.Column(db.String(20))
    entrance = db.Column(db.String(10))
    floor = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Integer, nullable=False)


class OrderStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('order_status.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)
    fat = db.Column(db.Float)
    carbohydrates = db.Column(db.Float)
    comment = db.Column(db.Text)
    timestamp = db.Column(db.TIMESTAMP)
    rating_id = db.Column(db.Integer, db.ForeignKey('rating.id'))


class OrderDish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class DishRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    rating_id = db.Column(db.Integer, db.ForeignKey('rating.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


def get_or_create(model, filters):
    data = model.query.filter_by(**filters).first()

    if not data:
        data = model(**filters)
        db.session.add(data)
        db.session.commit()

    return data