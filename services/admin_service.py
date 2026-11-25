"""Features for the Admin role: full CRUD on programs, workshops, jobs (Member 2)."""
from database import queries
from utils.inputs import ask_text, ask_int, confirm

# For each manageable item: table, list function, add function, prompts, editable fields.
ITEMS = {
    "program": {
        "table": "training_programs",
        "list": queries.list_programs,
        "add": lambda: queries.add_program(
            ask_text("Name: "), ask_text("Talent field: "), ask_text("Location: "),
            ask_text("Contact: "), ask_text("Description: ")),
        "fields": ["program_name", "talent_field", "location", "contact_info", "description"],
    },
    "workshop": {
        "table": "workshops",
        "list": queries.list_workshops,
        "add": lambda: queries.add_workshop(
            ask_text("Title: "), ask_text("Date: "), ask_text("Location: "), ask_int("Max spots: ", minimum=1)),
        "fields": ["title", "date", "location", "max_spots"],
    },
    "job": {
        "table": "jobs",
        "list": queries.list_jobs,
        "add": lambda: queries.add_job(
            ask_text("Title: "), ask_text("Category: "), ask_text("Contact: "), ask_text("How to apply: ")),
        "fields": ["title", "category", "contact_info", "instructions"],
    },
}


def manage(kind):
    item = ITEMS[kind]
    while True:
        print(f"\n--- MANAGE {kind.upper()}S ---")
        for row in item["list"]():
            print("  ", " | ".join(str(c) for c in row))
        print("\n  1. Add   2. Edit   3. Delete   0. Back")
        choice = ask_text("Choose: ", required=False)
        if choice == "1":
            item["add"]()
            print(f"{kind.capitalize()} added.")
        elif choice == "2":
            row_id = ask_int("ID to edit: ", minimum=1)
            print("Fields:", ", ".join(item["fields"]))
            field = ask_text("Field to change: ")
            if field not in item["fields"]:
                print("Unknown field.")
                continue
            value = ask_int("New value: ", minimum=1) if field == "max_spots" else ask_text("New value: ")
            print("Updated." if queries.update_row(item["table"], row_id, field, value) else "ID not found.")
        elif choice == "3":
            row_id = ask_int("ID to delete: ", minimum=1)
            if confirm("Delete permanently?"):
                print("Deleted." if queries.delete_row(item["table"], row_id) else "ID not found.")
        elif choice == "0":
            return
        else:
            print("Invalid choice.")


def view_registrations():
    print("\n--- ALL WORKSHOP REGISTRATIONS ---")
    rows = queries.list_all_registrations()
    if not rows:
        print("No registrations yet.")
    for rid, name, phone, title, when in rows:
        print(f"  #{rid} {name} ({phone}) -> {title} on {when}")
