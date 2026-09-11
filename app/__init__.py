import os

from flask import Flask

from config import config


def create_app(config_name=None):
    """Application factory pattern."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    # Project root is one level up from this package (app/)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app = Flask(
        __name__,
        template_folder=os.path.join(project_root, 'templates'),
        static_folder=os.path.join(project_root, 'templates', 'static'),
    )
    app.config.from_object(config[config_name])

    # Ensure database directory exists
    db_dir = os.path.dirname(app.config['DATABASE_PATH'])
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Register blueprints (imported inside factory to avoid circular imports)
    from app.routes import main  # noqa: C0415
    app.register_blueprint(main)

    # Error handlers (imported inside factory to avoid circular imports)
    from app.error_handlers import register_error_handlers  # noqa: C0415
    register_error_handlers(app)

    return app
