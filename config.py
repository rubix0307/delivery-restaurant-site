import os
import dotenv

dotenv.load_dotenv('.env')

DEBUG = True
SECRET_KEY = os.environ['SECRET_KEY']





