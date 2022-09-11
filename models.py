import os
from sqla_wrapper import SQLAlchemy

db_url = os.getenv("DATABSE_URL", "sqlite:///localhost.sqlite").replace("postgres://", "postgresl://", 1)
db = SQLAlchemy(db_url)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False )
    email = db.Column(db.String, unique=False)
    secret_number = db.Column(db.String, unique=False)