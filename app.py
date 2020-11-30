from flask import Flask, request, render_template, redirect, flash, session
from sqlalchemy import desc, asc
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'cluckcluck'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def list_users():
    """List all Users"""
    users = User.query.filter().order_by(User.last_name.asc(), User.first_name.asc())

    return render_template('list.html', users=users)

@app.route('/users/new')
def show_create_user_form():
    """Get view for create user form"""
    return render_template('create-form.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    image_url = request.form['imageUrl']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:user_id>')
def get_user_details(user_id):
    user = User.query.get_or_404(user_id)
    full_name = user.get_full_name()
    return render_template('details.html', user=user, full_name=full_name)

@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    full_name = user.get_full_name()
    return render_template('edit-form.html', user=user, full_name=full_name)

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

# 404 Error handling
@app.errorhandler(404) 
def not_found(e): 
  return render_template('404.html') 

