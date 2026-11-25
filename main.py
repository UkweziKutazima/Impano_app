"""IMPANO APP entry point: login, then a role-based menu loop (Member 3)."""
from database.schema import init_db
from services import auth_service, user_service, admin_service
from utils.inputs import ask_text


def youth_menu(user):
    while True:
        print("\n==================================================")
        print(f"  IMPANO APP | Youth: {user[1]}")
        print("==================================================")
        print(" 1. Search talent paths & training centers")
        print(" 2. Discover job and business opportunities")
        print(" 3. Register for a workshop")
        print(" 4. My workshop registrations (change / cancel)")
        print(" 5. My favorite programs")
        print(" 0. Log out")
        choice = ask_text("\nChoose (0-5): ", required=False)
        if choice == "1":
            user_service.search_programs(user)
        elif choice == "2":
            user_service.discover_jobs(user)
        elif choice == "3":
            user_service.register_workshop(user)
        elif choice == "4":
            user_service.my_registrations(user)
        elif choice == "5":
            user_service.view_favorites(user)
        elif choice == "0":
            return
        else:
            print("Invalid choice.")


def admin_menu(user):
    while True:
        print("\n==================================================")
        print(f"  IMPANO APP | Admin: {user[1]}")
        print("==================================================")
        print(" 1. Manage training programs")
        print(" 2. Manage workshops")
        print(" 3. Manage job opportunities")
        print(" 4. View all workshop registrations")
        print(" 0. Log out")
        choice = ask_text("\nChoose (0-4): ", required=False)
        if choice == "1":
            admin_service.manage("program")
        elif choice == "2":
            admin_service.manage("workshop")
        elif choice == "3":
            admin_service.manage("job")
        elif choice == "4":
            admin_service.view_registrations()
        elif choice == "0":
            return
        else:
            print("Invalid choice.")


def main():
    init_db()
    while True:
        print("\n==================================================")
        print("  WELCOME TO IMPANO APP")
        print("==================================================")
        print(" 1. Log in")
        print(" 2. Create youth account")
        print(" 0. Exit")
        choice = ask_text("\nChoose (0-2): ", required=False)
        if choice == "1":
            user = auth_service.log_in()
            if user:
                (admin_menu if user[5] == "admin" else youth_menu)(user)
        elif choice == "2":
            auth_service.sign_up()
        elif choice == "0":
            print("Goodbye. Keep growing your talent!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
