import os
import dotenv

dotenv.load_dotenv('.env')

app_config = dict(
    debug=True,
    SECRET_KEY=os.environ['SECRET_KEY'],
    SQLALCHEMY_DATABASE_URI=os.environ['SQLALCHEMY_DATABASE_URI'],
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    UPLOAD_FOLDER='uploads',
)
MAX_ORDER_QUANTITY = 10


