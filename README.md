# IMPANO APP

A Python command-line app that helps young people discover non-academic talent paths, training centers, workshops and job opportunities. Built with Python and SQLite for the ALU Peer Learning Project II (Group 2: Education, Job Creation, Arts, Design and Culture).

## Problem
Many young people have talents in carpentry, music, sports and trades but do not know where to train, which workshops to attend, or where to find work. IMPANO puts that information in one place.

## Features
**Youth role:** create an account and log in, search training programs by talent, bookmark favorites, browse jobs, register for workshops, change or cancel a registration.

**Admin role:** add, edit and delete programs, workshops and jobs, and view all registrations.

## Run it
    python main.py

No packages to install (Python 3.8+). The database `impano.db` is created automatically on first run.
Default admin login: `admin` / `admin123`

## Project structure
    main.py                   menus and program loop
    database/connection.py    SQLite connection
    database/schema.py        tables and starter data
    database/queries.py       all SQL queries
    services/auth_service.py  sign up and log in
    services/user_service.py  youth features
    services/admin_service.py admin features
    utils/inputs.py           safe input helpers
    utils/security.py         password hashing

## Database tables
users, training_programs, workshops, workshop_registrations (links users and workshops), jobs, favorites (links users and programs).

## Team contributions
- Kim Berly Marilyse Ndayiragije: database (schema, queries, seed data),user
- Arthur NZIZA: main menu, login, validation, documentation, admin features
