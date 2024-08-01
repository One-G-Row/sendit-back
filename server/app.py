
from flask import Flask, jsonify, request, session, make_response
from flask_restful import Resource
from models import Destination, User, Parcel, Admin
from flask_bcrypt import generate_password_hash
from config import db, api, app
from flask_jwt_extended import  create_access_token, jwt_required, get_jwt_identity


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

class Admins(Resource):
    def get(self, admin_id=None):
        if admin_id:
            admin = Admin.query.get(admin_id)
            if not admin:
                return make_response(jsonify({'error': 'Admin not found'}), 404)
            return make_response(jsonify(admin.to_dict()), 200)
        else:
            admins = [admin.to_dict() for admin in Admin.query.all()]
            return make_response(jsonify(admins), 200)

api.add_resource(Admins, '/admins', '/admins/<int:admin_id>')

class Destinations(Resource):
    def get(self, destination_id=None):
        if destination_id:
            destination = Destination.query.get(destination_id)
            if not destination:
                return make_response(jsonify({'error': 'Destination not found'}), 404)
            return make_response(jsonify(destination.to_dict()), 200)
        else:
            destinations = [destination.to_dict() for destination in Destination.query.all()]
            return make_response(jsonify(destinations), 200)
    
    def post(self):
        data = request.get_json()
        if not data or not data.get('location'):
            return jsonify({'message': 'Missing location information'}), 400
        
        new_destination = Destination(
            location=data.get('location'),
            arrival_day=data.get('arrival_day')
        )
        db.session.add(new_destination)
        db.session.commit()
        return jsonify({'message': 'Destination created successfully'}), 201
    
    def put(self, destination_id):
        data = request.get_json()
        destination = Destination.query.get_or_404(destination_id)
        
        if 'location' in data:
            destination.location = data['location']
        if 'arrival_day' in data:
            destination.arrival_day = data['arrival_day']
        
        db.session.commit()
        return jsonify({'message': 'Destination updated successfully'}), 200
    
    def delete(self, destination_id):
        destination = Destination.query.get_or_404(destination_id)
        db.session.delete(destination)
        db.session.commit()
        return jsonify({'message': 'Destination deleted successfully'}), 200

api.add_resource(Destinations, '/destinations/<int:destination_id>')

class DestinationList(Resource):
    def get(self):
        destinations = [destination.to_dict() for destination in Destination.query.all()]
        return make_response(jsonify(destinations), 200)

api.add_resource(DestinationList, '/destinations')

# Define a simple home route
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the SendIT API!'}), 200

# Define routes for parcel management
@app.route('/parcels', methods=['POST'])
@jwt_required()
def create_parcel():
    data = request.get_json()
    if not data or not data.get('parcel_item') or not data.get('parcel_weight'):
        return jsonify({'message': 'Missing parcel information'}), 400

    current_user = get_jwt_identity()
    new_parcel = Parcel(
        parcel_item=data.get('parcel_item'),
        parcel_description=data.get('parcel_description'),
        parcel_weight=data.get('parcel_weight'),
        parcel_cost=data.get('parcel_cost'),
        parcel_status='Pending',
        user_id=current_user['id'],
        destination_id=data.get('destination_id')
    )
    db.session.add(new_parcel)
    db.session.commit()
    return jsonify({'message': 'Parcel created successfully'}), 201

@app.route('/parcels/<int:parcel_id>', methods=['GET'])
@jwt_required()
def get_parcel(parcel_id):
    parcel = Parcel.query.get_or_404(parcel_id)
    return jsonify({
        'id': parcel.id,
        'parcel_item': parcel.parcel_item,
        'parcel_description': parcel.parcel_description,
        'parcel_weight': parcel.parcel_weight,
        'parcel_cost': parcel.parcel_cost,
        'parcel_status': parcel.parcel_status,
        'user_id': parcel.user_id,
        'destination_id': parcel.destination_id
    }), 200

@app.route('/parcels/<int:parcel_id>', methods=['PUT'])
@jwt_required()
def update_parcel(parcel_id):
    data = request.get_json()
    parcel = Parcel.query.get_or_404(parcel_id)
    current_user = get_jwt_identity()

    if parcel.user_id != current_user['id']:
        return jsonify({'message': 'Unauthorized'}), 403

    if 'parcel_item' in data:
        parcel.parcel_item = data['parcel_item']
    if 'parcel_description' in data:
        parcel.parcel_description = data['parcel_description']
    if 'parcel_weight' in data:
        parcel.parcel_weight = data['parcel_weight']
    if 'parcel_cost' in data:
        parcel.parcel_cost = data['parcel_cost']
    if 'destination_id' in data:
        parcel.destination_id = data['destination_id']
    if 'parcel_status' in data:
        parcel.parcel_status = data['parcel_status']

    db.session.commit()
    return jsonify({'message': 'Parcel updated successfully'}), 200

@app.route('/parcels/<int:parcel_id>', methods=['DELETE'])
@jwt_required()
def delete_parcel(parcel_id):
    parcel = Parcel.query.get_or_404(parcel_id)
    current_user = get_jwt_identity()

    if parcel.user_id != current_user['id']:
        return jsonify({'message': 'Unauthorized'}), 403

    db.session.delete(parcel)
    db.session.commit()
    return jsonify({'message': 'Parcel deleted successfully'}), 200

@app.route('/admin/register', methods=['POST'])
def admin_register():
    data = request.get_json()
    if Admin.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Admin already exists'}), 400
    new_admin = Admin(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password']
    )
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({'message': 'Admin created successfully'}), 201

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    admin = Admin.query.filter_by(email=data['email']).first()

    if admin and admin.verify_password(data['password']):
        access_token = create_access_token(identity=admin.id)
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/admin/parcels/<int:parcel_id>/status', methods=['PUT'])
@jwt_required()
def admin_change_status(parcel_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()
    admin = Admin.query.get(current_user_id)
    if not admin:
        return jsonify({'message': 'You are not an admin'}), 403
    
    parcel = Parcel.query.get_or_404(parcel_id)
    parcel.parcel_status = data['parcel_status']
    db.session.commit()
    return jsonify({'message': 'Status updated successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
