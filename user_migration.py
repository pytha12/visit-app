import os
from config import db
from models import User

# Fixture/Sample data
USERS = [
    {
        "fname": "Richard",
        "lname": "Guttman"
    },
    {
        "fname": "Adrian",
        "lname": "Schauer"
    },
    {
        "fname": "Scott",
        "lname": "Overhill"
    },
]

# Drop/Delete db file if already exists.
if os.path.exists("user_visit.db"):
    os.remove("user_visit.db")

# Create db
db.create_all()

# populate user table with users
for user in USERS:
    p = User(
        lname=user.get("lname"), 
        fname=user.get("fname")
    )
    db.session.add(p)
db.session.commit()
