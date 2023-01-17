"""Seed file to add data to Bogly database"""
from models import db, User, Post
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add users
alanAlda = User(first_name="Alan", last_name="Alda", image_url='https://upload.wikimedia.org/wikipedia/commons/2/21/Alan_Alda_2015.jpg')

joelBurton = User(first_name="Joel", last_name="Burton", image_url='http://joelburton.com/joel-burton.jpg')

janeSmith = User (first_name="Jane", last_name='Smith', image_url="https://media.licdn.com/dms/image/C5603AQFy1FW36jQ_9g/profile-displayphoto-shrink_800_800/0/1554238614307?e=2147483647&v=beta&t=HbFkDJItqOB079UxxyuhANVfdv3VafSwQgbM2ZCk0cM")


# Add posts
firstPost = Post(title="First Post!", content="oh, hai.", user_id="2")
anotherPost= Post(title="Yet Another Post", content="Ok, I'm posting again", user_id="2")
flaskIsAwesome= Post(title="Flask is Awesome", content="I just love Flask", user_id="2")

# Add new objects to session so they'll persist

db.session.add_all([alanAlda, joelBurton, janeSmith])
db.session.add_all([firstPost, anotherPost, flaskIsAwesome])
# db.session.add(joelBurton)
# db.session.add(janeSmith)

# Commit -- otherwise this never gets saved

db.session.commit()

