from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# MODELS GO BELOW!
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False)
    last_name = db.Column(db.String(50),
                     nullable=False)
    image_url = db.Column(db.String(200),
                     nullable=False)
    # full_name = db.Column(db.String(100),
    #                  nullable=False)

    def __repr__(self):
        user = self
        return f'<User - id: {user.id} first_name: {user.first_name} last_name: {user.last_name} image_url: {user.image_url}>'

    def get_full_name(self):
        user = self
        return f'{user.first_name} {user.last_name}'
    
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(280), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Post - title: {self.title} created_at: {self.created_at}>'

    def get_formatted_date(self):
        created_at = self.created_at
        year = created_at.year
        month = created_at.strftime("%B")
        day = created_at.strftime("%d")
        date = f'{month} {day}, {year}'
        time = f'{created_at.strftime("%I")}:{created_at.strftime("%M")} {created_at.strftime("%p")}'
        
        return f'{date}, {time}'

    user = db.relationship('User', backref='posts')                
