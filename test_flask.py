import flask_unittest

from unittest import TestCase
from app import app
from models import db, User

app.config['TESTING']=True
app.config['DEBUG_TB_HOSTS']=['dont-show-debug-toobar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests views for User"""
    def setUp(self):
        """Add a sample user BEFORE every test method is run"""
        User.query.delete()
        user=User(first_name="Test", last_name="User", image_url='https://media.licdn.com/dms/image/C4D03AQFHsvV_22jQ2w/profile-displayphoto-shrink_200_200/0/1516886455037?e=1678924800&v=beta&t=C6WJpxgHoFhwyYUNv49MpWfWQCOXtSuiwJllTYdzJRk')
        
        db.session.add(user)
        db.session.commit()

        self.user_id=user.id
        self.user=user
    
    def tearDown(self):
        """clean up any fouled transactions AFTER every test method is run"""
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp=client.get('/users')
            html =resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)
        
    def test_show_details(self):
        with app.test_client() as client:
            resp=client.get(f"/users/{self.user_id}")
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<title>Users</title>', html)
            self.assertIn(self.user.first_name, html)

    def test_create_user(self):
        with app.test_client() as client:
            d={"firstname": "Test", "lastname": "User", "imageURL": "https://media.licdn.com/dms/image/C4D03AQFHsvV_22jQ2w/profile-displayphoto-shrink_200_200/0/1516886455037?e=1678924800&v=beta&t=C6WJpxgHoFhwyYUNv49MpWfWQCOXtSuiwJllTYdzJRk"}

            resp=client.post('/users/new', data=d, follow_redirects=True)
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Users</h1>", html)

    def test_edit_user(self):
        with app.test_client() as client: 
            resp = client.get(f"/users/{self.user_id}/edit", follow_redirects=True)
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button type="submit" id="Button5">Save</button>', html) 