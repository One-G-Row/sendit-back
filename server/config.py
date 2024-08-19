import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///sendit.db')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'group 3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
CORS(app)

# Initialize Flask-RESTful API
api = Api(app)

# Define your routes and resources
# For example:
# from your_resources import SomeResource
# api.add_resource(SomeResource, '/some-endpoint')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
