from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import pymongo
import os
import motor.motor_asyncio

# MONGO_INITDB_ROOT_USERNAME="admin"
# MONGO_INITDB_ROOT_PASSWORD="password123"
MONGO_INITDB_DATABASE= "rakuten_db"

##Local
DATABASE_URL= 'mongodb://localhost:27017/'

##Docker
#DATABASE_URL = "mongodb://admin:password123@localhost:27017/"

SECRET_KEY = "19621424c891113672b114ef5128a555b7bb04ca431b5f9db66c1c56cb19f2ef"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

