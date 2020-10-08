import os


def load_config(app):

    app.secret_key = os.environ.get('SESSION_KEY')
    app.config['SESSION_TYPE'] = os.environ.get('SESSION_TYPE')
    app.config['MONGO_HOST'] = os.environ.get('MONGO_HOST')
    app.config['MONGO_PORT'] = os.environ.get('MONGO_PORT')
    app.config['MONGO_USER'] = os.environ.get('MONGO_USER')
    app.config['MONGO_PASSWORD'] = os.environ.get('MONGO_PASSWORD')
    app.config['MONGO_DB'] = os.environ.get('MONGO_DB')
    
    return app.config