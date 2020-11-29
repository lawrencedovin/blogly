from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
# from models import db, connect_db, Pet

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'cluckcluck'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    """Shows home page"""
    return render_template('home.html')

@app.route('/list')
def list_pets():
    """List pets and show add form."""

    pets = Pet.query.all()
    return render_template('list.html', pets=pets)

@app.route('/list', methods=['POST'])
def create_pet():
    name = request.form['name']
    species = request.form['species']
    hunger = request.form['hunger']
    hunger = int(hunger) if hunger else None

    new_pet = Pet(name=name, species=species, hunger=hunger)
    db.session.add(new_pet)
    db.session.commit()

    return redirect(f'/{new_pet.id}')

@app.route('/<int:pet_id>')
def get_pet_details(pet_id):
    """Shows specific details of pet"""

    pet = Pet.query.get_or_404(pet_id)

    return render_template('pet-details.html', pet=pet)

@app.route('/species/<species_id>')
def show_pets_by_species(species_id):
    pets = Pet.get_by_species(species_id)
    return render_template('species.html', pets=pets, species=species_id)

# 404 Error handling
@app.errorhandler(404) 
def not_found(e): 
  return render_template('404.html') 

