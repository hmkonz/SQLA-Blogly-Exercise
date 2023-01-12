"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)

app.app_context().push()


@app.route('/')
def show_users():
    users=User.query.all()
    return redirect('/users')

@app.route('/users')
def list_users():
    """Shows list of all the users in the db"""
    users=User.query.all()
    return render_template('all_users.html', users=users)


@app.route('/users/new', methods = ['GET', 'POST'])
def create_user():
     # if form has inputs to send along with request do the following; else go back to create_user.html template
    if request.method == 'POST':
       # retrieve inputs from form 
        firstName=request.form['firstname']
        lastName=request.form['lastname']
        imageURL=request.form['imageURL']
        # model User expects data to be in the format first_name, last_name and image_url so set those arguments equal to the variables from the form data retrieved above
        new_user=User(first_name=firstName, last_name=lastName, image_url=imageURL)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/users')
    else:
        """# if no inputs in the form, show the form for creating new users again"""
        return render_template('create_user.html')

    
   
@app.route('/user/{{user.id}}')
def show_details(user_id):
    """Show details about single user"""
    user=User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)


@app.route('/user/edit')
def edit_user(user_id):
    """Show user form to edit"""
    user=User.query.get(user_id)
    return render_template('edit_user.html', user_id)





