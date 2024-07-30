from flask import Flask, jsonify, request, session, make_response
from flask_restful import Resource
from models import User
from flask_bcrypt import generate_password_hash

class Users(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        return make_response(jsonify(user.to_dict()), 200)
    
    def patch(self, user_id):
        data = request.get_json()
        user = User.query.get(user_id)
        user.email = data['email']
        user.password = data['password']
        db.session.commit()
        return make_response(jsonify(user.to_dict()), 200)
    
    def delete(self, user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

class UserList(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(jsonify(users), 200)
    
    def post(self):
        data = request.get_json()
        if not data:
            return {'error': 'No data provided'}, 400
        try:
           hashed_password = generate_password_hash(data['password'])
           user = User(
              email = data['email'],
              password_hash = hashed_password
           )
           """ db.session.add(user)
           db.session.commit() """
        except Exception as e:
           print("Error:", e) 
           """ db.session.rollback() """
           return {'error': str(e)}, 400
    
api.add_resource(UserList, '/users')
api.add_resource(Users, '/users/<int:user_id>')