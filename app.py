from flask import Flask, request, render_template, redirect, flash, session
from sqlalchemy import desc, asc
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'cluckcluck'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def list_users():
    """List all Users"""
    users = User.query.filter().order_by(User.last_name.asc(), User.first_name.asc())

    return render_template('user-list.html', users=users)

@app.route('/users/new')
def show_create_user_form():
    """Get view for create user form"""
    
    return render_template('form/user/create-user.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    image_url = request.form['imageUrl']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/')

@app.route('/users/<int:user_id>')
def get_user_details(user_id):
    user = User.query.get_or_404(user_id)
    full_name = user.get_full_name()

    return render_template('details/user.html', user=user, full_name=full_name)

@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    full_name = user.get_full_name()

    return render_template('form/user/edit-user.html', user=user, full_name=full_name)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['firstName']
    user.last_name = request.form['lastName']
    user.image_url = request.form['imageUrl']

    db.session.commit()

    return redirect('/')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/')

@app.route('/users/<int:user_id>/posts/new')
def show_add_post_form(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('form/post/add-post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    title = request.form['postTitleInput']
    content = request.form['postContentInput']

    post = Post(title=title, content=title, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def get_post_details(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get(post.user_id)

    return render_template('details/post.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.user

    return render_template('form/post/edit-post.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['postTitleInput']
    post.content = request.form['postContentInput']

    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id

    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f'/users/{user_id}')

# 404 Error handling
@app.errorhandler(404) 
def not_found(e): 

  return render_template('404.html') 

