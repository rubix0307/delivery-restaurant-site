import os
import dotenv

dotenv.load_dotenv('.env')

DEBUG = True
SECRET_KEY = os.environ['SECRET_KEY']
SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']




