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

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
   

    def __repr__(self):
            """Show info about user"""
            p=self
            return f"<User {p.id} {p.first_name} {p.last_name} {p.image_url}>"



class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable =False)
    content = db.Column(db.Text, nullable =False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


    def __repr__(self):
            """Show info about post"""
            p=self
            return f"<Post {p.id} {p.title} {p.user_id}>"



class PostTag(db.Model):
    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    def __repr__(self):
            """Show info about post_tag"""
            p=self
            return f"<PostTag{p.post_id} {p.tag_id}>" 
            
class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique = True)

    posts = db.relationship("Post", secondary = "post_tags", backref = "tags")

    def __repr__(self):
            """Show info about tag"""
            p=self
            return f"<Tag {p.id} {p.name}>" 

