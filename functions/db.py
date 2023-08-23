from sqlalchemy import create_engine, MetaData, Column, Integer, String, Float, Text, Boolean, ForeignKey, TIMESTAMP
from config import app_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(app_config.get('SQLALCHEMY_DATABASE_URI'), echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine,
                                         ))
metadata = MetaData()
Base = declarative_base(metadata=metadata)
Base.query = db_session.query_property()

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    photo = Column(String(255))

    def __str__(self):
        return f'<Category {self.id}>'

    def __repr__(self):
        return self.__str__()

class Dish(Base):
    __tablename__ = 'dish'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    name_normal = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    available = Column(Boolean, default=True)
    photo = Column(String(255))
    weight = Column(Integer)
    calories = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    carbohydrates = Column(Float)

    def __str__(self):
        return f'<Dish {self.id}>'

    def __repr__(self):
        return self.__str__()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    email = Column(String(100), nullable=False)
    salt = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    telegram_id = Column(String(50))
    role_id = Column(Integer, ForeignKey('user_role.id'), nullable=False, default=1)

    def __str__(self):
        return f'<User {self.id}>'

    def __repr__(self):
        return self.__str__()


class UserAddress(Base):
    __tablename__ = 'user_address'
    id = Column(Integer, primary_key=True)
    city = Column(String(100), nullable=False)
    street = Column(String(100), nullable=False)
    house = Column(String(20), nullable=False)
    apartment = Column(String(20))
    entrance = Column(String(10))
    floor = Column(String(10))
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return f'<UserAddress {self.id}>'

    def __repr__(self):
        return self.__str__()


class Rating(Base):
    __tablename__ = 'rating'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    value = Column(Integer, nullable=False)

    def __str__(self):
        return f'<Rating {self.id}>'

    def __repr__(self):
        return self.__str__()


class OrderStatus(Base):
    __tablename__ = 'order_status'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    def __str__(self):
        return f'<OrderStatus {self.id}>'

    def __repr__(self):
        return self.__str__()


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    address_id = Column(Integer, ForeignKey('user_address.id'), nullable=False)
    status_id = Column(Integer, ForeignKey('order_status.id'), nullable=False)
    price = Column(Float, nullable=False)
    calories = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    carbohydrates = Column(Float)
    comment = Column(Text)
    timestamp = Column(TIMESTAMP)
    rating_id = Column(Integer, ForeignKey('rating.id'))

    def __str__(self):
        return f'<Order {self.id}>'

    def __repr__(self):
        return self.__str__()


class OrderDish(Base):
    __tablename__ = 'order_dish'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    dish_id = Column(Integer, ForeignKey('dish.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return f'<OrderDish {self.id}>'

    def __repr__(self):
        return self.__str__()


class DishRating(Base):
    __tablename__ = 'dish_rating'
    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey('dish.id'), nullable=False)
    rating_id = Column(Integer, ForeignKey('rating.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __str__(self):
        return f'<DishRating {self.id}>'

    def __repr__(self):
        return self.__str__()


class UserRole(Base):
    __tablename__ = 'user_role'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    def __str__(self):
        return f'<UserRole {self.id}>'

    def __repr__(self):
        return self.__str__()


def get_or_create(model, filters):
    data = model.query.filter_by(**filters).first()

    if not data:
        data = model(**filters)
        db_session.add(data)
        db_session.commit()

    return data