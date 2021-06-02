import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# instantiate the extensions
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.ext.stackdriver.trace_exporter import StackdriverExporter
from opencensus.trace.propagation import google_cloud_format
from opencensus.trace.samplers import AlwaysOnSampler

db = SQLAlchemy()
migrate = Migrate()
propagator = google_cloud_format.GoogleCloudFormatPropagator()


def createMiddleWare(app, exporter):
    """
    Configure a flask middleware that listens for each request and applies automatic tracing.
    This needs to be set up before the application starts.
    :param app: WSGI application
    :param exporter: Exporter instance object (StackdriverExporter)
    :return:
    """
    middleware = FlaskMiddleware(
        app,
        exporter=exporter,
        propagator=propagator,
        sampler=AlwaysOnSampler())
    return middleware


def app_factory():
    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    # Instrument Flask to do tracing automatically
    createMiddleWare(app, StackdriverExporter())
    return app
