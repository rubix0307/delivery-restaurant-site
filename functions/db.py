from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Text, Boolean, ForeignKey, TIMESTAMP
from config import app_config


metadata = MetaData()
engine = create_engine(app_config.get('SQLALCHEMY_DATABASE_URI'), echo=True)

category = Table(
    'category',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column('slug', String(100), nullable=False),
    Column('photo', String(255)),
)

dish = Table(
    'dish',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column('name_normal', String(100), nullable=False),
    Column('slug', String(100), nullable=False),
    Column('price', Float, nullable=False),
    Column('description', Text),
    Column('category_id', Integer, ForeignKey('category.id'), nullable=False),
    Column('available', Boolean, default=True),
    Column('photo', String(255)),
    Column('weight', Integer),
    Column('calories', Float),
    Column('protein', Float),
    Column('fat', Float),
    Column('carbohydrates', Float)
)

user_role = Table(
    'user_role',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False)
)

user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column('phone', String(15), nullable=False),
    Column('email', String(100), nullable=False),
    Column('salt', String(255), nullable=False),
    Column('password', String(255), nullable=False),
    Column('telegram_id', String(50)),
    Column('role_id', Integer, ForeignKey('user_role.id'), nullable=False, default=1)
)

user_address = Table(
    'user_address',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('city', String(100), nullable=False),
    Column('street', String(100), nullable=False),
    Column('house', String(20), nullable=False),
    Column('apartment', String(20)),
    Column('entrance', String(10)),
    Column('floor', String(10)),
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False)
)

rating = Table(
    'rating',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column('value', Integer, nullable=False)
)

order_status = Table(
    'order_status',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False)
)

order = Table(
    'order',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('address_id', Integer, ForeignKey('user_address.id'), nullable=True),
    Column('status_id', Integer, ForeignKey('order_status.id'), nullable=False),
    Column('price', Float, nullable=True),
    Column('calories', Float, nullable=True),
    Column('protein', Float, nullable=True),
    Column('fat', Float, nullable=True),
    Column('carbohydrates', Float, nullable=True),
    Column('comment', Text, nullable=True),
    Column('timestamp', TIMESTAMP, nullable=True),
    Column('rating_id', Integer, ForeignKey('rating.id'), nullable=True)
)

order_dish = Table(
    'order_dish',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('order_id', Integer, ForeignKey('order.id'), nullable=False),
    Column('dish_id', Integer, ForeignKey('dish.id'), nullable=False),
    Column('quantity', Integer, nullable=False),
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False)
)

dish_rating = Table(
    'dish_rating',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('dish_id', Integer, ForeignKey('dish.id'), nullable=False),
    Column('rating_id', Integer, ForeignKey('rating.id'), nullable=False),
    Column('user_id', Integer, ForeignKey('user.id'))
)
