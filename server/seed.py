from app import app, db
from models import Parcel, Destination, User, Admin
from faker import Faker
from random import choice as rc

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

        # Seed Admins
        admins = [
            Admin(first_name="Charles", last_name="Kagoko", email="chalokagoko@gmail.com", password="charles123"),
            Admin(first_name="Faith", last_name="Kimaru", email="faith@gmail.com", password="faith123"),
            Admin(first_name="Paul", last_name="Saitabau", email="paul@gmail.com", password="paul123"),
            Admin(first_name="Alvin", last_name="Kyle", email="alvin@gmail.com", password="alvin123"),
            Admin(first_name="Teddy", last_name="Kiplagat", email="teddy@gmail.com", password="teddy123"),
            Admin(first_name="Ted", last_name="Muigai", email="ted@gmail.com", password="muigai123"),  # New Admin
            Admin(first_name=fake.first_name(), last_name=fake.last_name(), email=fake.email(), password="password123")
        ]
        db.session.add_all(admins)

        # Seed Destinations
        destinations = []
        for _ in range(5):
            destination = Destination(
                location=fake.city()
            )
            destinations.append(destination)
        db.session.add_all(destinations)

        # Define specific items and descriptions
        item_descriptions = {
            "Electronics": "A delicate electronic device, handle with care.",
            "Furniture": "Large item, ensure it is securely packed.",
            "Clothing": "Seasonal clothing items, various sizes.",
            "Books": "A collection of books, some may be fragile.",
            "Groceries": "Food items, packed with care to prevent spoilage.",
            "Toys": "Children's toys, ensure they are packed safely.",
            "Jewelry": "Valuable jewelry items, handle with utmost care.",
            "Sports Equipment": "Outdoor gear, packed to prevent damage."
        }

        # Seed Parcels
        for user in User.query.all():
            for _ in range(5):
                parcel_item = rc(list(item_descriptions.keys()))
                parcel_description = item_descriptions[parcel_item]
                parcel = Parcel(
                    parcel_item=parcel_item,
                    parcel_description=parcel_description,
                    parcel_weight=round(fake.random_number(digits=2), 2),
                    parcel_cost=round(fake.random_number(digits=2), 2),
                    parcel_status=rc(['Pending', 'In Transit', 'Delivered']),
                    user_id=user.id,
                    destination_id=rc([d.id for d in Destination.query.all()])
                )
                db.session.add(parcel)

        db.session.commit()
        print("Seeding complete.")
