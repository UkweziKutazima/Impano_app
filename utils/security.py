"""Password hashing (Member 1)."""
import hashlib
import secrets


def hash_password(password):
    salt = secrets.token_hex(8)
    digest = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${digest}"


def verify_password(password, stored):
    salt, digest = stored.split("$")
    return hashlib.sha256((salt + password).encode()).hexdigest() == digest
