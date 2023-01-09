"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""

    db.app=app
    db.init_app(app)

class User(db.Model):
    

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(10), nullable =False)
    last_name = db.Column(db.String(20), nullable =False)
    image_url = db.Column(db.String(400), nullable=False)

    def __repr__(self):
            """Show info about user"""
            p=self
            return f"<User{p.id}{p.first_name}{p.last_name}{p.image_url}>"