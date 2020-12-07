from flask import Flask, request, render_template, redirect, flash, session
from sqlalchemy import desc, asc
from flask_debugtoolbar import DebugToolbarExtension
from models import *

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

    return render_template('list/user.html', users=users)

@app.route('/users/new')
def show_create_user_form():
    """Get view for create user form"""
    
    return render_template('form/user/create-user.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

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
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

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
    tags = Tag.query.all()

    return render_template('form/post/add/post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tag')

    post = Post(title=title, content=title, user_id=user_id)

    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name).one()
        post.tags.append(tag)
    
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def get_post_details(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.user

    return render_template('details/post.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.user
    tags = Tag.query.all()

    return render_template('form/post/edit/post.html', post=post, user=user, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    # Empty tags list first when added updating new tags 
    post.tags = []
    tags = request.form.getlist('tag')

    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name).one()
        post.tags.append(tag)
    
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id

    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/tags')
def list_tags():
    tags = Tag.query.filter().order_by(Tag.name.asc())

    return render_template('/list/tag.html', tags=tags)

@app.route('/tags/new')
def show_add_tag_form():
    return render_template('/form/post/add/tag.html')

@app.route('/tags/new', methods=['POST'])
def add_tag():
    name = request.form['name']

    new_tag = Tag(name=name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def get_tag_details(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    db.session.add(tag)
    db.session.commit()

    return render_template('details/tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    return render_template('form/post/edit/tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    db.session.commit()

    return redirect(f'/tags/{tag.id}')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    Tag.query.filter_by(id = tag_id).delete()
    db.session.commit()

    return redirect('/tags')


# 404 Error handling
@app.errorhandler(404) 
def not_found(e): 

  return render_template('404.html') 

