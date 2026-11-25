"""Features for the Youth role (Member 2)."""
from database import queries
from utils.inputs import ask_text, ask_int, confirm


def search_programs(user):
    print("\n--- SEARCH TALENT PATHS & TRAINING CENTERS ---")
    talent = ask_text("Enter your talent path (Carpentry, Music, Sports, Trades): ")
    results = queries.search_programs(talent)
    if not results:
        print(f"No programs found for '{talent}'.")
        return
    for pid, name, field, location, contact, desc in results:
        print(f"\n  [{pid}] {name} ({field})\n      Location: {location}\n      Contact:  {contact}\n      About:    {desc}")
    choice = ask_text("\nBookmark a program? Enter its ID or press Enter to skip: ", required=False)
    if choice.isdigit() and int(choice) in [r[0] for r in results]:
        queries.add_favorite(user[0], int(choice))
        print("Saved to your favorites.")


def view_favorites(user):
    print("\n--- YOUR FAVORITE PROGRAMS ---")
    favs = queries.list_favorites(user[0])
    if not favs:
        print("No favorites yet.")
        return
    for pid, name, field, location, contact in favs:
        print(f"  [{pid}] {name} ({field}) | {location} | {contact}")
    remove = ask_text("Enter an ID to remove it, or press Enter to go back: ", required=False)
    if remove.isdigit():
        if queries.remove_favorite(user[0], int(remove)):
            print("Removed.")
        else:
            print("That ID is not in your favorites.")


def discover_jobs(user):
    print("\n--- JOB & BUSINESS OPPORTUNITIES ---")
    category = ask_text("Enter a category (Arts, Trades, Sports): ")
    jobs = queries.search_jobs(category)
    if not jobs:
        print(f"No jobs found under '{category}'.")
        return
    for _id, title, cat, contact, how in jobs:
        print(f"\n  - {title} [{cat}]\n    Contact: {contact}\n    How to apply: {how}")


def _print_workshops(workshops):
    for wid, title, date, location, _max, left in workshops:
        print(f"  ID {wid}: {title} | {date} | {location} | Spots left: {left}")


def register_workshop(user):
    print("\n--- REGISTER FOR A WORKSHOP ---")
    _print_workshops(queries.list_workshops())
    workshop = queries.get_workshop(ask_int("\nWorkshop ID: ", minimum=1))
    if not workshop:
        print("Workshop not found.")
        return
    if workshop[5] <= 0:
        print("Sorry, this workshop is full.")
        return
    try:
        queries.register_for_workshop(user[0], workshop[0])
        print("Registration successful!")
    except Exception:
        print("You are already registered for this workshop.")


def my_registrations(user):
    print("\n--- MY WORKSHOP REGISTRATIONS ---")
    regs = queries.get_user_registrations(user[0])
    if not regs:
        print("You have no registrations.")
        return
    for rid, title, date, location, reg_date in regs:
        print(f"  Registration {rid}: {title} | {date} | {location} (registered {reg_date})")
    print("\n  1. Change to another workshop   2. Cancel a registration   0. Back")
    choice = ask_text("Choose: ", required=False)
    if choice == "1":
        rid = ask_int("Registration ID to change: ", minimum=1)
        _print_workshops(queries.list_workshops())
        new = queries.get_workshop(ask_int("New workshop ID: ", minimum=1))
        if not new or new[5] <= 0:
            print("That workshop does not exist or is full.")
        else:
            try:
                done = queries.change_registration(rid, user[0], new[0])
                print("Registration updated." if done else "Registration ID not found.")
            except Exception:
                print("You are already registered for that workshop.")
    elif choice == "2":
        rid = ask_int("Registration ID to cancel: ", minimum=1)
        if confirm("Are you sure?"):
            print("Registration cancelled." if queries.cancel_registration(rid, user[0]) else "Registration ID not found.")
