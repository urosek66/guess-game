import os
from sqla_wrapper import SQLAlchemy

# db = SQLAlchemy("sqlite:///db.sqlite")
db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False )
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    secret_number = db.Column(db.Integer, unique=False)
    session_token = db.Column(db.String)
    deleted = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, unique=False)
    best_score = db.Column(db.Integer, unique=False)