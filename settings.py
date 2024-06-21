# database
import os

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///{}/sql_app.db".format(CUR_PATH)


# token
SECRET_KEY = "b2eaa36336769d21afa6c70006d8d778c295b89d4bb7c137352f7d1f43aa0b5d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
