import sqlite3
from datetime import datetime

DB_NAME = "impano.db"


# ==========================================
# DATABASE SETUP & INITIAL SEED DATA (0x0D)
# ==========================================
def init_db():
    """Creates the database tables and adds starter data if empty."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Training Programs Table (Thing 1)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS training_programs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            program_name TEXT NOT NULL,
            talent_field TEXT NOT NULL,
            location TEXT NOT NULL,
            contact_info TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)

    # 2. Workshops Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workshops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            location TEXT NOT NULL,
            max_spots INTEGER NOT NULL
        )
    """)

    # 3. Workshop Registrations Table (Thing 2)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workshop_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attendee_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            workshop_title TEXT NOT NULL,
            registration_date TEXT NOT NULL
        )
    """)

    # 4. Job & Business Opportunities Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            contact_info TEXT NOT NULL,
            instructions TEXT NOT NULL
        )
    """)

    # Populate starter data if the tables are empty
    cursor.execute("SELECT COUNT(*) FROM training_programs")
    if cursor.fetchone()[0] == 0:
        sample_programs = [
            ("Bujumbura Woodcraft Hub", "Carpentry", "Ntahangwa, Bujumbura", "+257 79 111 222", "Hands-on furniture making and modern joinery."),
            ("East Africa Creative Studio", "Music", "Rohero, Bujumbura", "+257 79 333 444", "Audio production, vocals, and instrument mentorship."),
            ("Intamba Youth Athletics", "Sports", "Prince Louis Rwagasore Stadium", "+257 79 555 666", "Track, football coaching, and sports discipline."),
            ("Kigali-Bujumbura Tailoring Guild", "Trades", "Buyenzi, Bujumbura", "+257 79 777 888", "Commercial fashion design and garment construction.")
        ]
        cursor.executemany("""
            INSERT INTO training_programs (program_name, talent_field, location, contact_info, description)
            VALUES (?, ?, ?, ?, ?)
        """, sample_programs)

    cursor.execute("SELECT COUNT(*) FROM workshops")
    if cursor.fetchone()[0] == 0:
        sample_workshops = [
            ("Valuing Non-Academic Talents", "Nov 30, 2026", "Bujumbura Youth Center", 30),
            ("Turning Your Craft Into a Business", "Dec 05, 2026", "Kamenge Community Hall", 25),
            ("Sports & Creative Arts Mentorship Day", "Dec 12, 2026", "Rohero Arts Space", 40)
        ]
        cursor.executemany("""
            INSERT INTO workshops (title, date, location, max_spots)
            VALUES (?, ?, ?, ?)
        """, sample_workshops)

    cursor.execute("SELECT COUNT(*) FROM jobs")
    if cursor.fetchone()[0] == 0:
        sample_jobs = [
            ("Junior Furniture Maker", "Trades", "jobs@woodcrafthub.bi", "Call or visit the Ntahangwa workshop with a sample of your work."),
            ("Live Event Sound Assistant", "Arts", "studio@eacreative.bi", "Send a WhatsApp message with your availability."),
            ("Assistant Youth Football Coach", "Sports", "+257 79 555 666", "Apply in person on Saturday mornings at the stadium.")
        ]
        cursor.executemany("""
            INSERT INTO jobs (title, category, contact_info, instructions)
            VALUES (?, ?, ?, ?)
        """, sample_jobs)

    conn.commit()
    conn.close()


# ==========================================
# FEATURE 1: SEARCH PROGRAMS BY TALENT PATH
# ==========================================
def search_programs(favorites):
    print("\n--- SEARCH TALENT PATHS & TRAINING CENTERS ---")
    talent_query = input("Please enter your talent path (e.g., Carpentry, Music, Sports, Trades): ").strip()

    if not talent_query:
        print("Input cannot be empty. Returning to Main Menu...")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, program_name, talent_field, location, contact_info, description
        FROM training_programs
        WHERE LOWER(talent_field) LIKE ?
    """, (f"%{talent_query.lower()}%",))
    results = cursor.fetchall()
    conn.close()

    if not results:
        print(f"\nNo training programs found matching '{talent_query}'.")
    else:
        print(f"\nHere are the nearby training centers and program locations for '{talent_query}':")
        for row in results:
            prog_id, name, field, location, contact, desc = row
            print(f"\n  [{prog_id}] {name} ({field})")
            print(f"      Location: {location}")
            print(f"      Contact:  {contact}")
            print(f"      About:    {desc}")

        # Bonus Feature: Save to session favorites
        save_fav = input("\nWould you like to bookmark a program ID to your Favorites? (Enter ID or press Enter to skip): ").strip()
        if save_fav.isdigit():
            fav_id = int(save_fav)
            for row in results:
                if row[0] == fav_id:
                    if row not in favorites:
                        favorites.append(row)
                        print(f"Bookmarked '{row[1]}' to your session favorites!")
                    else:
                        print("That program is already in your favorites.")
                    break

    print("\nReturning to Main Menu...")


# ==========================================
# FEATURE 2: REGISTER FOR WORKSHOP
# ==========================================
def register_workshop():
    print("\n--- REGISTER FOR AWARENESS WORKSHOPS ---")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, date, location, max_spots FROM workshops")
    workshops = cursor.fetchall()

    print("Available Workshops:")
    for w in workshops:
        # Count current registrations to check remaining space
        cursor.execute("SELECT COUNT(*) FROM workshop_registrations WHERE workshop_title = ?", (w[1],))
        taken = cursor.fetchone()[0]
        spots_left = w[4] - taken
        print(f"  ID {w[0]}: {w[1]} | Date: {w[2]} | Location: {w[3]} | Spots Left: {spots_left}")

    # Exception handling (0x05) to stop crashes if user enters letters
    try:
        workshop_id = int(input("\nEnter the Workshop ID you want to join: ").strip())
    except ValueError:
        print("Invalid input. Please enter a valid number for the Workshop ID.")
        conn.close()
        return

    cursor.execute("SELECT title, max_spots FROM workshops WHERE id = ?", (workshop_id,))
    selected = cursor.fetchone()

    if not selected:
        print("Workshop ID not found. Returning to Main Menu...")
        conn.close()
        return

    workshop_title, max_spots = selected
    cursor.execute("SELECT COUNT(*) FROM workshop_registrations WHERE workshop_title = ?", (workshop_title,))
    taken = cursor.fetchone()[0]

    if taken >= max_spots:
        print("Sorry, this workshop is already full! Returning to Main Menu...")
        conn.close()
        return

    attendee_name = input("Enter your full name: ").strip()
    phone_number = input("Enter your phone number: ").strip()

    if not attendee_name or not phone_number:
        print("Name and phone number are required. Registration cancelled.")
        conn.close()
        return

    reg_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
        INSERT INTO workshop_registrations (attendee_name, phone_number, workshop_title, registration_date)
        VALUES (?, ?, ?, ?)
    """, (attendee_name, phone_number, workshop_title, reg_date))

    conn.commit()
    conn.close()

    print("\nRegistration successful! Further workshop details will be sent to your phone number via message.")
    print("Returning to Main Menu...")


# ==========================================
# FEATURE 3: DISCOVER JOB OPPORTUNITIES
# ==========================================
def discover_jobs():
    print("\n--- DISCOVER JOB & BUSINESS OPPORTUNITIES ---")
    category = input("Enter a skill category (e.g., Arts, Trades, Sports): ").strip()

    if not category:
        print("Category cannot be empty. Returning to Main Menu...")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, category, contact_info, instructions
        FROM jobs
        WHERE LOWER(category) LIKE ?
    """, (f"%{category.lower()}%",))
    jobs = cursor.fetchall()
    conn.close()

    if not jobs:
        print(f"\nNo open job listings found under '{category}'.")
    else:
        print(f"\nOpen Opportunities in '{category}':")
        for job in jobs:
            title, cat, contact, instructions = job
            print(f"\n  - Role:         {title} [{cat}]")
            print(f"    Contact:      {contact}")
            print(f"    How to Apply: {instructions}")

    print("\nReturning to Main Menu...")


# ==========================================
# BONUS FEATURE: VIEW SAVED FAVORITES
# ==========================================
def view_favorites(favorites):
    print("\n--- YOUR BOOKMARKED PROGRAMS (THIS SESSION) ---")
    if not favorites:
        print("You haven't bookmarked any training programs yet.")
    else:
        for fav in favorites:
            print(f"  - {fav[1]} ({fav[2]}) | Location: {fav[3]} | Contact: {fav[4]}")
    print("\nReturning to Main Menu...")


# ==========================================
# MAIN MENU LOOP (0x01 & 0x02)
# ==========================================
def main():
    init_db()
    session_favorites = []  # List to store bookmarked programs during session

    while True:
        print("\n==================================================")
        print("  WELCOME TO IMPANO APP")
        print("==================================================")
        print("What would you like to do today?")
        print(" 1. Search talent paths & training centers")
        print(" 2. Register for awareness workshops")
        print(" 3. Discover job and business opportunities")
        print(" 4. View bookmarked favorite programs (Bonus)")
        print(" 0. Exit program")

        choice = input("\nType a number (0-4) and press Enter: ").strip()

        if choice == "1":
            search_programs(session_favorites)
        elif choice == "2":
            register_workshop()
        elif choice == "3":
            discover_jobs()
        elif choice == "4":
            view_favorites(session_favorites)
        elif choice == "0":
            print("\nThank you for using IMPANO APP. Keep growing your talent! Goodbye.")
            break
        else:
            print("\nInvalid choice! Please type 0, 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
