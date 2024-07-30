
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

                # Seed Admins
        admins = [
            Admin(first_name="Charles", last_name="Kagoko", email="chalokagoko@gmailcom", password_hash="charles123"),
            Admin(first_name="Faith", last_name="Kimaru", email="faith@gmailcom", password_hash="faith123"),
            Admin(first_name="Paul", last_name="Saitabau", email="paul@gmailcom", password_hash="paul123"),
            Admin(first_name="Alvin", last_name="Kyle", email="alvin@gmailcom", password_hash="alvin123"),
            Admin(first_name="Teddy", last_name="Kiplagat", email="teddy@gmailcom", password_hash="teddy123"),
            Admin(first_name=fake.first_name(), last_name=fake.last_name(), email=fake.email(), password_hash="password123")
        ]
        db.session.add_all(admins)

        # Seed Destinations
        destinations = [
            Destination(location="Nairobi"),
            Destination(location="Kisumu"),
            Destination(location="Mombasa"),
            Destination(location="Nakuru"),
            Destination(location="Eldoret"),
            Destination(location="Kiambu")
        ]
        for _ in range(5):
            destination = Destination(
                arrival_day=fake.date_tim)




