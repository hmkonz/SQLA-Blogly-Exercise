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

    
   
@app.route('/users/<user_id>')
def show_details(user_id):
    """Show details about single user"""
    user=User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)


@app.route('/users/<user_id>/edit', methods = ['GET', 'POST'])
def edit_user(user_id):
    # if 'edit user form' has modifications to be saved and sent along with request, do the following; else return to details page if cancel or update the user
    if request.method == 'POST':
        # retrieve inputs from form 
        # firstName=request.form['firstname']
        # lastName=request.form['lastname']
        # imageURL=request.form['imageURL']
        # model User expects data to be in the format first_name, last_name and image_url so set those arguments equal to the variables from the form data retrieved above

        # get the data for the user having their data edited.
        updated_user=User.query.filter_by(user_id={{user_id}})
        # update the data by assigning it to what's in the form
        updated_user.first_name=request.form['firstname']
        updated_user.last_name=request.form['lastname']
        updated_user.image_url=request.form['imageURL']
        
        db.session.add(updated_user)
        db.session.commit()

        return redirect('/users/<user_id>')
    else:
        """Show user form to edit"""
        user=User.query.get_or_404(user_id)
        return render_template('edit_user.html', user=user)


@app.route('/users/<user_id>/delete', methods = ['POST'])
def delete_user(user_id):
    "Delete user and show updated list of users"
    # User.query.get_or_404(user_id)
    User.query.filter_by(user_id=={{user_id}}).delete()
    db.session.commit()
    return redirect ('/users')


