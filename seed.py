"""Seed file to add data to Bogly database"""
from models import db, User
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
alanAlda = User(first_name="Alan", last_name="Alda", image_url='https://upload.wikimedia.org/wikipedia/commons/2/21/Alan_Alda_2015.jpg')

joelBurton = User(first_name="Joel", last_name="Burton", image_url='http://joelburton.com/joel-burton.jpg')

janeSmith = User (first_name="Jane", last_name='Smith', image_url="https://media.licdn.com/dms/image/C5603AQFy1FW36jQ_9g/profile-displayphoto-shrink_800_800/0/1554238614307?e=2147483647&v=beta&t=HbFkDJItqOB079UxxyuhANVfdv3VafSwQgbM2ZCk0cM")

# Add new objects to session so they'll persist

db.session.add(alanAlda)
db.session.add(joelBurton)
db.session.add(janeSmith)

# Commit -- otherwise this never gets saved

db.session.commit()