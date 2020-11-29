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
    
    # @classmethod
    # def get_by_species(cls, species):
    #     return cls.query.filter_by(species=species).all()
    
    # @classmethod
    # def get_all_hungry(cls):
    #     return cls.query.filter(cls.hunger > 10).all()

    # @classmethod
    # def delete_all_hungry(cls):
    #     cls.query.filter(cls.hunger == 100).delete()
    #     db.session.commit()

    def __repr__(self):
        user = self
        return f'<User id={user.id} first_name={user.first_name} last_name={user.last_name} image_url={user.image_url}>'

    def get_full_name(self):
        user = self
        return f"{user.first_name} {user.last_name}"

    # def greet(self):
    #     pet = self
    #     if pet.name == 'Cowboy':
    #         return f'Yeehaw mah name is {pet.name} and I am a {pet.species} from Texas.'
    #     return f'HI my name is {pet.name}, and I am a {pet.species} pls feed me.'
    
    # def feed(self, amt=20):
    #     """Update hunger based off of amt"""
    #     pet = self
    #     pet.hunger -= amt
    #     """Takes the max of each value if negative takes the new max value of 0"""
    #     self.hunger = max(self.hunger, 0)
                    
