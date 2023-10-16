"""Flask app for adopt app."""

from flask import Flask, url_for, render_template, redirect, flash, jsonify

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

# Set SQLAlchemy configuration directly
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'kiki_delivery_service'

# Connect the database
connect_db(app)

# Initialize the Debug Toolbar extension
toolbar = DebugToolbarExtension(app)


@app.route('/')
def pets_list():
    pets = Pet.query.all()
    return render_template('pets_list.html', pets=pets)


@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    form = AddPetForm()

    if form.validate_on_submit():
        data = {p: d for p, d in form.data.items() if p != "csrf_token"}
        new_pet = Pet(**data)
        db.session.add(new_pet)
        db.session.commit()
        flash(f'{new_pet.name} added.')
        return redirect(url_for('pets_list'))

    else:
        return render_template('add_pet.html', form=form)


@app.route("/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect(url_for('pets_list'))

    else:
        return render_template("pet_detail.html", form=form, pet=pet)


@app.route("/api/pets/<int:pet_id>", methods=['GET'])
def api_get_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    info = {'name': pet.name, 'age': pet.age}
    return jsonify(info)
