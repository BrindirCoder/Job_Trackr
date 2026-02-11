from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import Config
from .models import db, User

login_manager = LoginManager()
migrate = Migrate()
jwt = JWTManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    login_manager.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app
