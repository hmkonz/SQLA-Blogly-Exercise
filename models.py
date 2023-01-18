"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

import datetime

db = SQLAlchemy()

def connect_db(app):
        """Connect this database to provided Flask App"""

        db.app=app
        db.init_app(app)

class User(db.Model):
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable =False)
    last_name = db.Column(db.Text, nullable =False)
    image_url = db.Column(db.Text, nullable=False)

   

    def __repr__(self):
            """Show info about user"""
            p=self
            return f"<User{p.id}{p.first_name}{p.last_name}{p.image_url}>"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable =False)
    content = db.Column(db.Text, nullable =False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user=db.relationship('User', backref='posts')

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


    def __repr__(self):
            """Show info about user"""
            p=self
            return f"<Post{p.id}{p.title}{p.content}{p.created_at}{p.user_id}>" 
            
