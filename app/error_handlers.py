from flask import render_template


def register_error_handlers(app):
    """Register error handlers."""

    @app.errorhandler(404)
    def not_found_error(error):  # noqa: ARG001 (Flask passes the exception)
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):  # noqa: ARG001 (Flask passes the exception)
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):  # noqa: ARG001 (Flask passes the exception)
        return render_template('errors/403.html'), 403

    @app.errorhandler(400)
    def bad_request_error(error):  # noqa: ARG001 (Flask passes the exception)
        return render_template('errors/400.html'), 400
