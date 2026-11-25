"""All SQL lives here (Member 1). Services call these functions; they never write SQL."""
from datetime import datetime
from database.connection import get_connection

# Columns that may be edited per table (whitelist keeps update_row safe).
EDITABLE = {
    "training_programs": {"program_name", "talent_field", "location", "contact_info", "description"},
    "workshops": {"title", "date", "location", "max_spots"},
    "jobs": {"title", "category", "contact_info", "instructions"},
}


def _fetch(sql, params=()):
    conn = get_connection()
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return rows


def _execute(sql, params=()):
    """Run INSERT/UPDATE/DELETE. Returns (last row id, rows changed)."""
    conn = get_connection()
    cur = conn.execute(sql, params)
    conn.commit()
    result = (cur.lastrowid, cur.rowcount)
    conn.close()
    return result


# ---------- Users ----------
def create_user(full_name, phone, username, password_hash, role="youth"):
    return _execute(
        "INSERT INTO users (full_name, phone, username, password_hash, role) VALUES (?,?,?,?,?)",
        (full_name, phone, username, password_hash, role),
    )[0]


def get_user_by_username(username):
    rows = _fetch("SELECT id, full_name, phone, username, password_hash, role FROM users WHERE username = ?", (username,))
    return rows[0] if rows else None


# ---------- Generic UPDATE / DELETE for programs, workshops, jobs ----------
def update_row(table, row_id, field, value):
    if field not in EDITABLE[table]:
        raise ValueError("Field not editable")
    return _execute(f"UPDATE {table} SET {field} = ? WHERE id = ?", (value, row_id))[1]


def delete_row(table, row_id):
    return _execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))[1]


# ---------- Training programs ----------
def list_programs():
    return _fetch("SELECT id, program_name, talent_field, location, contact_info, description FROM training_programs")


def search_programs(talent):
    return _fetch(
        "SELECT id, program_name, talent_field, location, contact_info, description "
        "FROM training_programs WHERE LOWER(talent_field) LIKE ?",
        (f"%{talent.lower()}%",),
    )


def add_program(name, field, location, contact, description):
    return _execute(
        "INSERT INTO training_programs (program_name, talent_field, location, contact_info, description) VALUES (?,?,?,?,?)",
        (name, field, location, contact, description),
    )[0]


# ---------- Jobs ----------
def list_jobs():
    return _fetch("SELECT id, title, category, contact_info, instructions FROM jobs")


def search_jobs(category):
    return _fetch(
        "SELECT id, title, category, contact_info, instructions FROM jobs WHERE LOWER(category) LIKE ?",
        (f"%{category.lower()}%",),
    )


def add_job(title, category, contact, instructions):
    return _execute(
        "INSERT INTO jobs (title, category, contact_info, instructions) VALUES (?,?,?,?)",
        (title, category, contact, instructions),
    )[0]


# ---------- Workshops ----------
def list_workshops():
    """Each workshop with how many spots are left."""
    return _fetch(
        "SELECT w.id, w.title, w.date, w.location, w.max_spots, "
        "w.max_spots - COUNT(r.id) AS spots_left "
        "FROM workshops w LEFT JOIN workshop_registrations r ON r.workshop_id = w.id "
        "GROUP BY w.id"
    )


def get_workshop(workshop_id):
    rows = [w for w in list_workshops() if w[0] == workshop_id]
    return rows[0] if rows else None


def add_workshop(title, date, location, max_spots):
    return _execute(
        "INSERT INTO workshops (title, date, location, max_spots) VALUES (?,?,?,?)",
        (title, date, location, max_spots),
    )[0]


# ---------- Registrations ----------
def register_for_workshop(user_id, workshop_id):
    return _execute(
        "INSERT INTO workshop_registrations (user_id, workshop_id, registration_date) VALUES (?,?,?)",
        (user_id, workshop_id, datetime.now().strftime("%Y-%m-%d %H:%M")),
    )[0]


def get_user_registrations(user_id):
    return _fetch(
        "SELECT r.id, w.title, w.date, w.location, r.registration_date "
        "FROM workshop_registrations r JOIN workshops w ON w.id = r.workshop_id "
        "WHERE r.user_id = ?",
        (user_id,),
    )


def change_registration(registration_id, user_id, new_workshop_id):
    return _execute(
        "UPDATE workshop_registrations SET workshop_id = ? WHERE id = ? AND user_id = ?",
        (new_workshop_id, registration_id, user_id),
    )[1]


def cancel_registration(registration_id, user_id):
    return _execute(
        "DELETE FROM workshop_registrations WHERE id = ? AND user_id = ?",
        (registration_id, user_id),
    )[1]


def list_all_registrations():
    return _fetch(
        "SELECT r.id, u.full_name, u.phone, w.title, r.registration_date "
        "FROM workshop_registrations r "
        "JOIN users u ON u.id = r.user_id JOIN workshops w ON w.id = r.workshop_id"
    )


# ---------- Favorites ----------
def add_favorite(user_id, program_id):
    return _execute("INSERT OR IGNORE INTO favorites (user_id, program_id) VALUES (?,?)", (user_id, program_id))[1]


def list_favorites(user_id):
    return _fetch(
        "SELECT p.id, p.program_name, p.talent_field, p.location, p.contact_info "
        "FROM favorites f JOIN training_programs p ON p.id = f.program_id WHERE f.user_id = ?",
        (user_id,),
    )


def remove_favorite(user_id, program_id):
    return _execute("DELETE FROM favorites WHERE user_id = ? AND program_id = ?", (user_id, program_id))[1]
