""""Seed file to make sample data for blogly db."""

from models import *
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

# Add tags
fun_tag = Tag(name='Fun')
cool_tag = Tag(name='Cool')
hip_tag = Tag(name='Hip')
fancy_tag = Tag(name='Fancy')

# Add post tag relationships
first_fun_tag = PostTag(post_id=1, tag_id=1)
first_hip_tag = PostTag(post_id=1, tag_id=3)
puberty_fun_tag = PostTag(post_id=2, tag_id=1)
puberty_cool_tag = PostTag(post_id=2, tag_id=2)

# Add new object to session, so they'll persist
db.session.add_all([lawrence, julie, miguel])
db.session.add_all([post1, post2])
db.session.add_all([fun_tag, cool_tag, hip_tag, fancy_tag])

# Commit confirms changes and makes it permanent
db.session.commit()

# Add post to tag relationship after initial data has been entered
db.session.add_all([first_fun_tag, first_hip_tag, puberty_fun_tag, puberty_cool_tag])
db.session.commit()