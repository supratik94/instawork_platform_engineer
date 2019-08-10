__author__ = "Supratik Majumdar"
__status__ = "Development"

from flask import Flask
from .v0 import v0_blueprint


def create_app():
    app = Flask(__name__)

    app.register_blueprint(v0_blueprint)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
