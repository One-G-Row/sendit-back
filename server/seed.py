
from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Parcel, Destination, User, Admin

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        # Clear existing data
        Parcel.query.delete()
        Destination.query.delete()
        User.query.delete()
        Admin.query.delete()

        print("Starting seed...")

        # Seed Users
        users = []
        for _ in range(10):
            user = User(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                _password_hash='password123'  # Default password
            )
            users.append(user)
        db.session.add_all(users)



