"""Table creation and starter data (Member 1)."""
from database.connection import get_connection
from utils.security import hash_password

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'youth'))
);
CREATE TABLE IF NOT EXISTS training_programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_name TEXT NOT NULL,
    talent_field TEXT NOT NULL,
    location TEXT NOT NULL,
    contact_info TEXT NOT NULL,
    description TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS workshops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT NOT NULL,
    location TEXT NOT NULL,
    max_spots INTEGER NOT NULL CHECK (max_spots > 0)
);
CREATE TABLE IF NOT EXISTS workshop_registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    workshop_id INTEGER NOT NULL REFERENCES workshops(id) ON DELETE CASCADE,
    registration_date TEXT NOT NULL,
    UNIQUE (user_id, workshop_id)
);
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    contact_info TEXT NOT NULL,
    instructions TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS favorites (
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    program_id INTEGER NOT NULL REFERENCES training_programs(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, program_id)
);
"""

PROGRAMS = [
    ("Bujumbura Woodcraft Hub", "Carpentry", "Ntahangwa, Bujumbura", "+257 79 111 222", "Hands-on furniture making and modern joinery."),
    ("East Africa Creative Studio", "Music", "Rohero, Bujumbura", "+257 79 333 444", "Audio production, vocals, and instrument mentorship."),
    ("Intamba Youth Athletics", "Sports", "Prince Louis Rwagasore Stadium", "+257 79 555 666", "Track, football coaching, and sports discipline."),
    ("Kigali-Bujumbura Tailoring Guild", "Trades", "Buyenzi, Bujumbura", "+257 79 777 888", "Commercial fashion design and garment construction."),
]
WORKSHOPS = [
    ("Valuing Non-Academic Talents", "Nov 30, 2026", "Bujumbura Youth Center", 30),
    ("Turning Your Craft Into a Business", "Dec 05, 2026", "Kamenge Community Hall", 25),
    ("Sports & Creative Arts Mentorship Day", "Dec 12, 2026", "Rohero Arts Space", 40),
]
JOBS = [
    ("Junior Furniture Maker", "Trades", "jobs@woodcrafthub.bi", "Call or visit the Ntahangwa workshop with a sample of your work."),
    ("Live Event Sound Assistant", "Arts", "studio@eacreative.bi", "Send a WhatsApp message with your availability."),
    ("Assistant Youth Football Coach", "Sports", "+257 79 555 666", "Apply in person on Saturday mornings at the stadium."),
]


def init_db():
    """Create tables and insert starter data on first run."""
    conn = get_connection()
    conn.executescript(SCHEMA)
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        conn.execute(
            "INSERT INTO users (full_name, phone, username, password_hash, role) VALUES (?,?,?,?,?)",
            ("System Admin", "+257 00 000 000", "admin", hash_password("admin123"), "admin"),
        )
    if conn.execute("SELECT COUNT(*) FROM training_programs").fetchone()[0] == 0:
        conn.executemany("INSERT INTO training_programs (program_name, talent_field, location, contact_info, description) VALUES (?,?,?,?,?)", PROGRAMS)
    if conn.execute("SELECT COUNT(*) FROM workshops").fetchone()[0] == 0:
        conn.executemany("INSERT INTO workshops (title, date, location, max_spots) VALUES (?,?,?,?)", WORKSHOPS)
    if conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0] == 0:
        conn.executemany("INSERT INTO jobs (title, category, contact_info, instructions) VALUES (?,?,?,?)", JOBS)
    conn.commit()
    conn.close()
