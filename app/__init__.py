from flask import Flask
from app.extensions import db, jwt, cors, mail
from app.routes import auth, feedback, analytics, translate


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_pyfile('../config.py')

db = SQLAlchemy(app)
jwt = JWTManager(app)
mail = Mail(app)

from app import routes

def create_app():
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    mail.init_app(app)

    # Register blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(feedback.bp)
    app.register_blueprint(analytics.bp)
    app.register_blueprint(translate.bp)

    return app
