import logging
import os
from flask import Flask, jsonify, render_template, request

from .db import init_app as init_db
from .logging_config import setup_logging
from .services import ValidationError, NotFoundError


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)
    app.config["DATABASE"] = os.path.join(app.instance_path, "expenses.db")
    if test_config:
        app.config.update(test_config)

    setup_logging(app)
    init_db(app)

    from .routes import bp
    app.register_blueprint(bp)

    @app.errorhandler(ValidationError)
    def handle_validation(err):
        logging.getLogger(__name__).warning("Validation failed: %s", err)
        if request.path.startswith("/api/"):
            return jsonify(error=str(err)), 400
        from . import services
        return render_template("index.html", error=str(err),
                               expenses=services.list_expenses(),
                               summary=services.summary(),
                               categories=services.CATEGORIES), 400

    @app.errorhandler(NotFoundError)
    def handle_not_found(err):
        return jsonify(error=str(err)), 404

    @app.errorhandler(Exception)
    def handle_unexpected(err):
        code = getattr(err, "code", None)
        if isinstance(code, int) and code < 500:
            return jsonify(error=getattr(err, "description", "Error")), code
        logging.getLogger(__name__).exception("Unhandled error")
        return jsonify(error="Internal server error"), 500

    return app
