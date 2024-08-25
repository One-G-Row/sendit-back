from flask_restful import Api
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__, static_folder="moringa/phase5/sendit/sendIT-group-3-client/build", static_url_path="/")
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SECRET_KEY'] = 'group 3' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
api = Api(app)

frontend_folder = os.path.join(os.getcwd(), "..", "moringa", "phase5", "sendit", "sendIT-group-3-client", "build")
dist_folder = os.path.join(frontend_folder, "dist")

@app.route("/", defaults={'filename': ''})
@app.route("/<path:filename>")
def index(filename):
   if not filename:
     filename = "index.html"   
   return send_from_directory(dist_folder, filename)
     

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

#api routes

with app.app_context():
    db.create_all()