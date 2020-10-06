from nubi_test.blueprints.alive import alive_bp

def register_blueprints(app):
    app.register_blueprint(alive_bp, url_prefix='/api/alive')