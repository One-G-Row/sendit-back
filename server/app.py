from flask import Flask, jsonify, request, make_response, session
from flask_restful import Resource
from models import Destination, User, Parcel, Admin
from config import db, api, app
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import  create_access_token, jwt_required, get_jwt_identity

class ClearSession(Resource):
    def delete(self):
        session['page_views'] = None
        session['user_id'] = None

class Signup(Resource):
    def get(self):
        return {}, 200
    
    def post(self):
        data = request.get_json()
        if not data:
            return {'error': 'No data provided'}, 400
        try:
            hashed_password = generate_password_hash(data['password'])
            user = User(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                password_hash = hashed_password
            )
            db.session.add(user)
            db.session.commit()
            return make_response(jsonify(user.to_dict()), 201)
        except Exception as e:
            print("Error:", e)
            db.session.rollback()
            return {'error': str(e)}, 400

class CheckSession(Resource):
    def get(self):
        user = User.query.filter_by(id=session.get('user_id')).first()
        if user:
            response = jsonify(user.to_dict), 200
            return response
        else:
            return {}, 204
        
class LoginUser(Resource):
    def post(self):
        user = User.query.filter(User.email == request.get_json()['email']).first()
        if user:
            session['user_id'] = user.id
            response = make_response(jsonify(user.to_dict()), 200)
            return response 
        else:
            return {}, 401
           
class LoginAdmin(Resource):
    def post(self):
        admin = Admin.query.filter(Admin.email == request.get_json())['email'].first()
        if admin:
            session['admin_id'] = admin.id
            response = make_response(jsonify(admin.to_dict()), 200)
            return response
        else:
            return {}, 401
        
class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {}, 204
        
# Define User-related endpoints
class Users(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return make_response(jsonify(user.to_dict()), 200)
        return make_response(jsonify({'error': 'User not found'}), 404)
    
    def patch(self, user_id):
        data = request.get_json()
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({'error': 'User not found'}), 404)
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password_hash = generate_password_hash(data['password'])
        
        db.session.commit()
        return make_response(jsonify(user.to_dict()), 200)
    
    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({'error': 'User not found'}), 404)
        
        db.session.delete(user)
        db.session.commit()
        return {}, 204

class UserList(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(jsonify(users), 200)
    
    def post(self):
        data = request.get_json()
        if not data:
            return {'error': 'No data provided'}, 400
        try:
           if 'password' not in data:
               return {'error': 'Password is required'}, 400

           hashed_password = generate_password_hash(data['password'])
           user = User(
              first_name = data['first_name'],
              last_name = data['last_name'],
              email = data['email'],
              password = hashed_password
           )
           db.session.add(user)
           db.session.commit() 
           return make_response(jsonify(user.to_dict(), 201))
        
        except Exception as e:
           print("Error:", e) 
           db.session.rollback()
           return {'error': str(e)}, 400
    
api.add_resource(LoginUser, '/loginuser', endpoint='loginuser')
api.add_resource(LoginAdmin, '/loginadmin', endpoint='loginadmin')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(Users, '/users/<int:user_id>', endpoint='user')

# Define Admin-related endpoints
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

# Define home route
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the SendIT API!'}), 200

# Define parcel-related endpoints
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
#@jwt_required()
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
#@jwt_required()
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
#@jwt_required()
def delete_parcel(parcel_id):
    parcel = Parcel.query.get_or_404(parcel_id)
    current_user = get_jwt_identity()

    if parcel.user_id != current_user['id']:
        return jsonify({'message': 'Unauthorized'}), 403

    db.session.delete(parcel)
    db.session.commit()
    return jsonify({'message': 'Parcel deleted successfully'}), 200

# Define admin-related authentication endpoints
@app.route('/admin/register', methods=['POST'])
def admin_register():
    data = request.get_json()
    try:
        # Access fields using the names from the client-side
        if Admin.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Admin already exists'}), 400

        hashed_password = generate_password_hash(data['password'])
        new_admin = Admin(
            first_name=data['first_name'],  
            last_name=data['last_name'],    
            email=data['email'],
            password_hash=hashed_password
        )
        db.session.add(new_admin)
        db.session.commit()
        return jsonify({'message': 'Admin created successfully'}), 201
    except Exception as e:
        print(f"Error occurred: {e}")  # Log the error
        return jsonify({'message': 'An error occurred while creating the admin'}), 500



@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    admin = Admin.query.filter_by(email=data['email']).first()

    if admin and check_password_hash(admin.password_hash, data['password']):
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

# Define destination-related endpoints
@app.route('/destinations/', methods=['GET'])
def get_destinations():
    destinations = [destination.to_dict() for destination in Destination.query.all()]
    return make_response(jsonify(destinations), 200)

@app.route('/destinations/<int:destination_id>', methods=['GET'])
def get_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if not destination:
        return jsonify({'message': 'Destination not found'}), 404
    return jsonify(destination.to_dict()), 200

@app.route('/destinations', methods=['POST'])
#@jwt_required()
def create_destination():
    data = request.get_json()
    if not data or not data.get('location') or not data.get('arrival_day'):
        return jsonify({'message': 'Missing destination information'}), 400

    try:
        arrival_day = datetime.strptime(data.get('arrival_day'), '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS'}), 400

    new_destination = Destination(
        location=data.get('location'),
        arrival_day = arrival_day
    )
    db.session.add(new_destination)
    db.session.commit()
    return jsonify({'message': 'Destination created successfully'}), 201

@app.route('/destinations/<int:destination_id>', methods=['PUT'])
#@jwt_required()
def update_destination(destination_id):
    data = request.get_json()
    destination = Destination.query.get(destination_id)
    if not destination:
        return jsonify({'message': 'Destination not found'}), 404

    if 'location' in data:
        destination.location = data['location']
    if 'arrival_day' in data:
        try:
            arrival_day = datetime.strptime(data['arrival_day'], '%Y-%m-%d %H:%M:%S')
            destination.arrival_day = arrival_day
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS'}), 400

    db.session.commit()
    return jsonify({'message': 'Destination updated successfully'}), 200

@app.route('/destinations/<int:destination_id>', methods=['DELETE'])
#@jwt_required()
def delete_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if not destination:
        return jsonify({'message': 'Destination not found'}), 404

    db.session.delete(destination)
    db.session.commit()
    return jsonify({'message': 'Destination deleted successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)