from mongoengine import connect

class MongoConn:
    def __init__(self, app):
        host = app.config['MONGO_HOST']
        port = app.config['MONGO_PORT']
        username = app.config['MONGO_USER']
        password = app.config['MONGO_PASSWORD']
        db_name = app.config['MONGO_DB']

        connect(
            db=db_name, host=f"mongodb://{username}:{password}@{host}:{port}/?authSource=admin")