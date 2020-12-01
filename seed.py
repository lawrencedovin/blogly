""""Seed file to make sample data for blogly db."""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
lawrence = User(first_name='Lawrence', last_name='Dovin', image_url='https://images.unsplash.com/photo-1517783999520-f068d7431a60?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1650&q=80')
julie = User(first_name='Julie', last_name='Paez', image_url='https://images.unsplash.com/photo-1517783999520-f068d7431a60?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1650&q=80')
miguel = User(first_name='Miguel', last_name='Servin', image_url='https://images.unsplash.com/photo-1517783999520-f068d7431a60?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1650&q=80')

# Add posts
post1 = Post(title='First Post!', content='Hello', user_id=1)
post2 = Post(title='Puberty the Horror', content='Bad', user_id=1)

# Add new object to session, so they'll persist
db.session.add_all([lawrence, julie, miguel])
db.session.add_all([post1, post2])

# Commit confirms changes and makes it permanent
db.session.commit()