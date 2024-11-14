from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def connect_to_mongo():
    try:
        # Connection URI to MongoDB service
        client = MongoClient('mongodb://mongo:27017/')  # 'mongo' is the name of the MongoDB container in Docker Compose

        # Access a specific database (this will create it if it doesn't exist)
        db = client.test_db

        # Check if the connection is successful by listing collections
        collections = db.list_collection_names()
        print(f"Connected to MongoDB. Collections in 'test_db': {collections}")

        # You can also perform further operations here, such as inserting or querying documents.

    except ConnectionFailure as e:
        print(f"Error while connecting to MongoDB: {e}")


if __name__ == "__main__":
    connect_to_mongo()
