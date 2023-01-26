"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
from flask_bootstrap import Bootstrap
import pdb


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
db.create_all()

@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)

# User routes

@app.route('/users')
def list_users():
    """Shows a page with info  on all the users in the db"""
    users=User.query.all()
    return render_template('all_users.html', users=users)


@app.route('/users/new', methods = ['GET', 'POST'])
def create_user():

    """Handle form submission for creating a new user"""

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
        """# As a GET request, show the form for  creating new users"""
        return render_template('create_user.html')

    
   
@app.route('/users/<int:user_id>')
def show_details(user_id):
    """Show a page with details about a specific user"""
    user=User.query.get_or_404(user_id)
    posts=Post.query.filter_by(user_id=user.id)
    return render_template('user_details.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit', methods = ['GET', 'POST'])
def edit_user(user_id):
    """Handle form submission for updating an existing user"""

    # if 'edit user form' has modifications to be saved and sent along with request, do the following; else return to details page if cancel 
  
    if request.method == 'POST': 
        
        # model User expects data to be in the format first_name, last_name and image_url so set these arguments equal to the form data
    
        # retrieve data of user editing their user info using their user_id 
        updated_user=User.query.get_or_404(user_id)
        
        # retrieve edited inputs from form and update first_name, last_name and image_url in the table
        updated_user.first_name=request.form['firstname']
        updated_user.last_name=request.form['lastname']
        updated_user.image_url=request.form['imageURL']
        
        db.session.add(updated_user)
        db.session.commit()
        # in python, use an'f string' with a dynamic user_id so can be redirected to the corresponding user detail page
        return redirect(f'/users/{user_id}')
    else:
        """As a GET request, show form to edit an existing user """
        user=User.query.get_or_404(user_id)
        return render_template('edit_user.html', user=user)


@app.route('/users/<user_id>/delete', methods = ['POST'])
def delete_user(user_id):
    """Handle form submission for deleting an existing user and showing updated list of users"""

    # retrieve data of user to be deleted using their user_id 
    delete_user=User.query.get_or_404(user_id)
    # delete user
    db.session.delete(delete_user)
    db.session.commit()
    return redirect ('/users')

# Post routes

@app.route('/users/<int:user_id>/posts/new', methods=["GET", "POST"])
def create_post(user_id):
    """Handle form submission for creating a new post for a specific user"""

    # retrieve data of user that's adding a post using their user_id 
    user=User.query.get_or_404(user_id)
    
    # retrieve all tags
    tags=Tag.query.all()

    # if form has inputs to send along with request do the following; else go back to create_post.html template
    if request.method == 'POST':
       # retrieve inputs from form 
        title=request.form['title']
        content=request.form['content']
        # retrieve all input values (tag.ids) of checkboxes that are checked
        selected_tags=request.form.getlist('tag_checkbox')
        # create empty list so selected tags can be added to it
        selected_tag_ids=[]

        # pdb.set_trace()

        # loop over all the selected tags and append each one (made into an integer with 
        # int(tag))to the selected_tag_ids list
        for tag in selected_tags:
            selected_tag_ids.append(int(tag))

        # retrieve all the tags with Tag.id in the selected_tag_ids list
        tags = Tag.query.filter(Tag.id.in_(selected_tag_ids)).all()

        # create a new_post with title, content and tags from the form as well as the user so post is added to a specific user
        new_post=Post(title=title, content=content, user=user, tags=tags)
       
        # add new post with checked tags to the database
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(f'/users/{user_id}')

    else:
        """# As a GET request, show the form for creating a new post"""
        
        return render_template('create_post.html', user=user, tags=tags)


@app.route('/posts/<post_id>')
def show_post_details(post_id):
    """Show a page with details about a specific post and its tags"""

    post=Post.query.get_or_404(post_id)
    post_tags=post.tags

    return render_template('post_details.html', post=post, post_tags=post_tags)
     

@app.route('/posts/<post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    """Handle form submission for updating an existing post"""

     # retrieve all tags
    tags=Tag.query.all()

    # if 'edit post form' has modifications to be saved and sent along with request, do the following; else return to details page if cancel 
  
    if request.method == 'POST': 
        
        # retrieve data of post using its post_id 
        updated_post=Post.query.get_or_404(post_id)
        
        # retrieve edited inputs from form and update post first_name, last_name and image_url in the table
        updated_post.title=request.form['title']
        updated_post.content=request.form['content']
        
        selected_tags=request.form.getlist('tag_checkbox')
        selected_tag_ids=[]

        for tag in selected_tags:
            selected_tag_ids.append(int(tag))

        updated_post.tags=Tag.query.filter(Tag.id.in_(selected_tag_ids)).all()

        updated_post=Post(title=updated_post.title, content=updated_post.content, tags=updated_post.tags)

        
        db.session.add(updated_post)
        db.session.commit()
        # in python, use an'f string' with a dynamic post_id so can be redirected to the corresponding post detail page
        return redirect(f'/posts/{post_id}')
    else:
        """As a GET request, show a form to edit an existing post"""
        post=Post.query.get_or_404(post_id)
        return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/delete', methods = ['POST'])
def delete_post(post_id):
    """Handle form submission for deleting an existing post and showing user detail page"""

    # retrieve data of post to be deleted using the post_id 
    delete_post=Post.query.get_or_404(post_id)
    # delete post
    db.session.delete(delete_post)
    db.session.commit()
    return redirect (f'/users/{delete_post.user_id}')


# Tag routes

@app.route('/tags')
def list_tags():
    """Shows a page with all the tags in the db"""

    tags=Tag.query.all()
    return render_template('all_tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """Show a page with details about a specific tag"""
    
    tag=Tag.query.get_or_404(tag_id)
    tag_posts=tag.posts
    return render_template('tag_details.html', tag=tag, tag_posts=tag_posts)

@app.route('/tags/new', methods=["GET", "POST"])
def create_tag():
    """Handle form submission for creating a new tag"""

    # if form has inputs to send along with request do the following; else go back to create_tag.html template
    if request.method == 'POST':
       # retrieve inputs from form 
        name=request.form['name']
        
        new_tag=Tag(name=name)

        db.session.add(new_tag)
        db.session.commit()
        return redirect('/tags')
    else:
        """# As a GET request, show the form for creating a new tag"""
        
        return render_template('create_tag.html')

@app.route('/tags/<int:tag_id>/edit', methods=["GET", "POST"])
def edit_tag(tag_id):
    """Handle form submission for updating an existing tag"""

    # if 'edit tag form' has modifications to be saved and sent along with request, do the following; else return to list of tags page if cancel 
  
    if request.method == 'POST':

        # retrieve data of tag using its tag_id   
        updated_tag=Tag.query.get_or_404(tag_id)
        
        # retrieve edited inputs from form and update name in the table
        updated_tag.name=request.form['name']
        
        
        db.session.add(updated_tag)
        db.session.commit()
     
        return redirect('/tags')
    else:
        """As a GET request, show a form to edit an existing tag"""
        tag=Tag.query.get_or_404(tag_id)
        return render_template('edit_tag.html', tag=tag)

    
@app.route('/tags/<int:tag_id>/delete', methods = ['POST'])
def delete_tag(tag_id):
    """Handle form submission for deleting an existing tag and showing list of tags page"""

    # retrieve data of tag to be deleted using the tag_id 
    deleted_tag=Tag.query.get_or_404(tag_id)
    # delete tag
    db.session.delete(deleted_tag)
    db.session.commit()
    return redirect ('/tags')
   