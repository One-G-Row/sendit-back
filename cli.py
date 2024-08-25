from config import app, db
from helpers import (
    exit_program,
    get_user_by_id,
    list_users, 
    create_user,
    delete_user,
    get_parcel_by_id,
    list_parcels,
    create_parcel,
    delete_parcel,
    get_admin_by_id,
    list_admins,
    get_destination_by_id,
    list_destinations,
    create_destination,
    delete_destination,
)

def main():
    with app.app_context():
        while True:
            menu()
            choice = input(" >")
            if choice == "0":
                    exit_program()
            elif choice == "1":
                list_users()
            elif choice == "2":
                id = input("Enter user ID: ")
                user = get_user_by_id(id)
                if user:
                    print(user)
                else:
                    print("User not found.")
            elif choice == "3":
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                email = input("Enter email: ")
                password = input("Enter password: ")
                create_user(first_name, last_name, email, password)
            elif choice == "4":
                id = input("Enter user ID: ")
                delete_user(id)
            elif choice == "5":
                list_parcels()
            elif choice == "6":
                id = input("Enter parcel ID: ")
                parcel = get_parcel_by_id(id)
                if parcel:
                    print(parcel)
                else:
                    print("Parcel not found.")
            elif choice == "7":
                item = input("Enter item: ")
                description = input("Enter description: ")
                weight = input("Enter weight: ")
                cost = input("Enter cost: ")
                status = input("Enter status: ")
                user_id = input("Enter user ID: ")
                destination_id = input("Enter destination ID: ")
                create_parcel(item, description, weight, cost, status, user_id, destination_id)
            elif choice == "8":
                id = input("Enter parcel ID: ")
                delete_parcel(id)
            elif choice == "9":
                list_admins()
            elif choice == "10":
                id = input("Enter admin ID: ")
                admin = get_admin_by_id(id)
                if admin:
                    print(admin)
                else:
                    print("Admin not found.")
            elif choice == "11":
                list_destinations()
            elif choice == "12":
                id = input("Enter destination ID: ")
                destination = get_destination_by_id(id)
                if destination:
                    print(destination)
                else:
                    print("Destination not found.")
            elif choice == "13":
                location = input("Enter location: ")
                arrival_day = input("Enter arrival day: ")
                create_destination(location, arrival_day)
            elif choice == "14":
                id = input("Enter destination ID: ")
                delete_destination(id)
            else:
                print("Invalid choice. Please try again.")

def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. List all users")
    print("2. Find user by ID")
    print("3. Create new user")
    print("4. Delete user by ID") 
    print("5. List all parcels")
    print("6. Find parcel by ID")
    print("7. Create new parcel")
    print("8. Delete parcel by ID") 
    print("9. List all admins")
    print("10. Find admin by ID") 
    print("11. List all destinations")
    print("12. Find destination by ID")
    print("13. Create new destination")   
    print("14. Delete destination by ID")
    
if __name__ == "__main__":
    main()          