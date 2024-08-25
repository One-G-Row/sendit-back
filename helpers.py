from flask import session
from models import User, Parcel, Admin, Destination
from config import db, app
from datetime import datetime

def exit_program():
    print("Goodbye!")
    exit()
def create_user(first_name, last_name, email, password):
    with app.app_context():
        user = User(first_name=first_name, last_name=last_name, email=email)
        user._password_hash=password
        db.session.add(user)
        db.session.commit()
        print("User created successfully.")

def get_user_by_id(user_id):
    with app.app_context():
        user = User.query.get(user_id)
        print((user.id, user.email))
        
def list_users():
    with app.app_context():
         users = User.query.all()
    for user in users:
        print({'ID': user.id, 'Email': user.email})

def delete_user(user_id):
    with app.app_context():
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        print("User deleted successfully.")

def create_parcel(parcel_item, parcel_description, parcel_weight, parcel_cost, parcel_status, user_id, destination_id):
    with app.app_context():
        parcel = Parcel(parcel_item=parcel_item, parcel_description=parcel_description, parcel_weight=parcel_weight, parcel_cost=parcel_cost, parcel_status=parcel_status, user_id=user_id, destination_id=destination_id)
        db.session.add(parcel)
        db.session.commit()
        print("Parcel created successfully.")

def get_parcel_by_id(parcel_id):
    with app.app_context():
        parcel = Parcel.query.get(parcel_id)
        print((parcel.id, parcel.parcel_item, parcel.parcel_description, parcel.parcel_weight, parcel.parcel_cost, parcel.parcel_status))
        
def list_parcels():
    with app.app_context():
         parcels = Parcel.query.all()
    for parcel in parcels:
        print({'ID': parcel.id, 'Item': parcel.parcel_item, 'Description': parcel.parcel_description, 'Weight': parcel.parcel_weight, 'Cost': parcel.parcel_cost, 'Status': parcel.parcel_status})

def delete_parcel(parcel_id):
    with app.app_context():
        parcel = Parcel.query.get(parcel_id)
        db.session.delete(parcel)
        db.session.commit()
        print("Parcel deleted successfully.")

def get_admin_by_id(admin_id):
    with app.app_context():
        admin = Admin.query.get(admin_id)
        print((admin.id, admin.first_name, admin.last_name, admin.email))
        
def list_admins():
    with app.app_context():
         admins = Admin.query.all()
    for admin in admins:
        print({'ID': admin.id, 'First Name': admin.first_name, 'Last Name': admin.last_name, 'Email': admin.email})

def create_destination(location, arrival_day_str):
    with app.app_context():
        try:
            arrival_day = datetime.strptime(arrival_day_str, "%Y-%m-%d").date()
        except ValueError as e:
            print(f"Invalid date format: {e}")
            return
        
        destination = Destination(location=location, arrival_day=arrival_day)
        db.session.add(destination)
        db.session.commit()
        print("Destination created successfully.")

def get_destination_by_id(destination_id):
    with app.app_context():
        destination = Destination.query.get(destination_id)
        print((destination.id, destination.location, destination.arrival_day))
        
def list_destinations():
    with app.app_context():
         destinations = Destination.query.all()
    for destination in destinations:
        print({'ID': destination.id, 'Location': destination.location, 'Arrival Day': destination.arrival_day})

def delete_destination(destination_id):
    with app.app_context():
        destination = Destination.query.get(destination_id)
        db.session.delete(destination)
        db.session.commit()
    print("Destination deleted successfully.")