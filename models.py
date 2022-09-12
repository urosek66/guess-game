import os
from sqla_wrapper import SQLAlchemy

# db = SQLAlchemy("sqlite:///db.sqlite")
db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True )
    email = db.Column(db.String, unique=True)
    secret_number = db.Column(db.Integer, unique=False)