import os
from flask import Flask

from nubi_test.init import config, register,logger

def start_server():
    app = create_app()
    return app


def init_app(app):
    app.config = config.load_config(app)
    app.logger = logger.configure_logger('app')
    MongoConn(app)  


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    
    with app.app_context():
        
        init_app(app)
        register.register_blueprints(app)

        return app