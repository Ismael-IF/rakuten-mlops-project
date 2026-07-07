from pymongo import mongo_client
import pymongo
from config.settings import *
from config.init_database import *
import time

##Local
#client = mongo_client.MongoClient(DATABASE_URL, serverSelectionTimeoutMS=5000)

## Docker
client = mongo_client.MongoClient(os.environ["DB_URL"], serverSelectionTimeoutMS=5000)

try:
    conn = client.server_info()
    print(f'Connected to MongoDB {conn.get("version")}')
    
except Exception:
    print("Unable to connect to the MongoDB server.")

db = client[MONGO_INITDB_DATABASE]
Users_db = db.rakuten_users
Users_db.create_index([("email", pymongo.ASCENDING)], unique=True)


try:
         print("Database Initialization ...")
         time.sleep(2)
         initialse_db(Users_db)
         print("Database Initialization done")
         time.sleep(2)
        
except pymongo.errors.DuplicateKeyError:
         print('Database initialization already done')
         pass
#else:
#        print("Unable to initialize Database. Check if MongoDB container is up and running...")

