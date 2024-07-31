from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object('server.config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

from server.models import User, Admin, Parcel, Destination  # Import models to register them with SQLAlchemy








# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_migrate import Migrate
# from flask_jwt_extended import JWTManager

# app = Flask(__name__)
# app.config.from_object('server.config.Config')

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# jwt = JWTManager(app)
# bcrypt = Bcrypt(app)

# from server.models import User, Admin, Parcel, Destination  # Import models to register them with SQLAlchemy
