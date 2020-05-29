from flask import Flask

from api.api import api
from api.models import db
from flask_site import site


def create_app():
    app = Flask(__name__)

    HOST = "34.71.196.78"
    USER = "root"
    PASSWORD = "root1234"
    DATABASE = "hireCar"

    app.config[
        "SQLALCHEMY_DATABASE_URI"] = f"mysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(api)
    app.register_blueprint(site)

    return app



def setup_clean_db(TEST_DB=True):
    app = create_app()
    HOST = "34.71.196.78"
    USER = "root"
    PASSWORD = "root1234"
    DATABASE = "hireCar"

    if TEST_DB:
        DATABASE += '_test'
    app.config[
        "SQLALCHEMY_DATABASE_URI"] = f"mysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}"
    with app.app_context():
        db.drop_all()
        db.create_all()


