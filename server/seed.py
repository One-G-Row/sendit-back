
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
                password='password123'  # Default password
            )
            users.append(user)
        db.session.add_all(users)
        db.session.commit()

                # Seed Admins
        admins = [
            Admin(first_name="Charles", last_name="Kagoko", email="chalokagoko@gmailcom", password="charles123"),
            Admin(first_name="Faith", last_name="Kimaru", email="faith@gmailcom", password="faith123"),
            Admin(first_name="Paul", last_name="Saitabau", email="paul@gmailcom", password="paul123"),
            Admin(first_name="Alvin", last_name="Kyle", email="alvin@gmailcom", password="alvin123"),
            Admin(first_name="Teddy", last_name="Kiplagat", email="teddy@gmailcom", password="teddy123"),
            Admin(first_name=fake.first_name(), last_name=fake.last_name(), email=fake.email(), password="password123")
        ]
        db.session.add_all(admins)
        db.session.commit()

        destinations = []
        for _ in range(10):
            destination = Destination(
                location=fake.city(),
                arrival_day=fake.date_time_between(start_date='-30d', end_date='+30d')
            )
            destinations.append(destination)
        db.session.add_all(destinations)
        db.session.commit()

         # Seed Parcels
        parcels = []
        for user in users:
            parcel = Parcel(
                parcel_item=fake.word(),
                parcel_description=fake.text(max_nb_chars=200),
                parcel_weight=rc([1.0, 2.5, 5.0, 10.0, 20.0]),
                parcel_cost=rc([50.0, 100.0, 200.0, 300.0]),
                parcel_status=rc(['Pending', 'Shipped', 'Delivered']),
                user_id=user.id
            )
            parcels.append(parcel)
        db.session.add_all(parcels)
        db.session.commit()  # Commit parcels to assign IDs

        # Seed Destinations
        for parcel in parcels:
            destination = Destination(
                location=fake.city(),
                arrival_day=fake.date_time_between(start_date='-30d', end_date='+30d'),
                parcel_id=parcel.id  # Link destination to parcel
            )
            db.session.add(destination)

        # Commit all changes
            db.session.commit()
        print("Data seeded successfully!")










