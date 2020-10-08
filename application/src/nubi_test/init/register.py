from nubi_test.blueprints.alive import alive_bp
from nubi_test.blueprints.poll import polls_bp
from nubi_test.blueprints.user import users_bp

def register_blueprints(app):
    app.register_blueprint(alive_bp, url_prefix='/api/alive')
    app.register_blueprint(polls_bp, url_prefix='/api/polls')
    app.register_blueprint(users_bp, url_prefix='/api/users')