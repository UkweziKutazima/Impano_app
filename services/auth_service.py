"""Sign up and log in (Member 3)."""
import sqlite3
from database import queries
from utils.inputs import ask_text
from utils.security import hash_password, verify_password


def sign_up():
    print("\n--- CREATE YOUTH ACCOUNT ---")
    full_name = ask_text("Full name: ")
    phone = ask_text("Phone number: ")
    username = ask_text("Choose a username: ")
    password = ask_text("Choose a password: ")
    try:
        queries.create_user(full_name, phone, username, hash_password(password), "youth")
        print("Account created. You can now log in.")
    except sqlite3.IntegrityError:
        print("That username is already taken.")


def log_in():
    """Return the user row if credentials are correct, else None."""
    print("\n--- LOG IN ---")
    username = ask_text("Username: ")
    password = ask_text("Password: ")
    user = queries.get_user_by_username(username)
    if user and verify_password(password, user[4]):
        print(f"\nWelcome, {user[1]}!")
        return user
    print("Wrong username or password.")
    return None
