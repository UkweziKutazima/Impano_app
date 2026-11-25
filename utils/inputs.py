"""Safe input helpers used by every menu (Member 3)."""


def ask_text(prompt, required=True):
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("  This field cannot be empty.")


def ask_int(prompt, minimum=None):
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print("  Please enter a valid number.")
            continue
        if minimum is not None and value < minimum:
            print(f"  Number must be at least {minimum}.")
            continue
        return value


def confirm(prompt):
    return input(f"{prompt} (y/n): ").strip().lower() == "y"
