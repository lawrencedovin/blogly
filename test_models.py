from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class PetModelTestCase(TestCase):
    """Tests for model for Pets."""

    def setUp(self):
        """Clean up any existing pets."""
        User.query.delete()
    
    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()
    
    def test_get_full_name(self):
        user = User(first_name='Lawrence', last_name='Dovin', image_url='https://images.unsplash.com/photo-1517783999520-f068d7431a60?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1650&q=80')
        self.assertEqual(user.get_full_name(), 'Lawrence Dovin')