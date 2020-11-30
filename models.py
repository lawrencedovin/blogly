from flask_sqlalchemy import SQLAlchemy

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
        return f'<User id={user.id} first_name={user.first_name} last_name={user.last_name} image_url={user.image_url}>'

    def get_full_name(self):
        user = self
        return f"{user.first_name} {user.last_name}"
                    
