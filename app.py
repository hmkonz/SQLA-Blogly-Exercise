"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)

app.app_context().push()



@app.route('/')
def list_users():
    """Shows list of all the users in the db"""
    users=User.query.all()
    return render_template('all_users.html', users=users)








