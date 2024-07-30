from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, bcrypt, User, Admin, Parcel, Destination
from config import app, jwt

# Initialize the app with configurations from config.py
app.config.from_object('config')