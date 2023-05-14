from flask import Flask, render_template, abort, request, redirect
from services.pokemon_service import get_pokemon_list
from services.pokemon_service import get_pokemon_details
from services.trainer_service import create_trainer, read_trainers, update_trainer, delete_trainer

app = Flask(__name__)

'''
index page
'''
@app.route("/")
def index():
    return render_template("index.html")

'''
pokedex page
'''
@app.route("/pokedex")
def pokemon():
    pokemon_list = get_pokemon_list()
    return render_template("pokedex.html", pokemon_list=pokemon_list)

'''
pokemon details page
'''
@app.route("/pokedex/<pokemon_id>")
def pokemon_details(pokemon_id):
    # Fetch the details of the specific Pokemon using the ID
    pokemon = get_pokemon_details(pokemon_id)

    if pokemon is None:
        # Handle the case if the Pokemon is not found
        # return "Pokemon not found"
        abort(404)

    return render_template("pokemon_details.html", pokemon=pokemon)

'''
404 page
'''
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

'''
Trainers page
'''
# Get all trainers & pokemons
@app.route('/trainers')
def trainers():
    trainers = read_trainers()
    return render_template('trainers.html', trainers=trainers)

# Creates trainer & pokemon
@app.route('/trainers', methods=['POST'])
def add_trainer():
    name = request.form.get('name')
    pokemon = request.form.get('pokemon')
    create_trainer(name, pokemon)  # Pass the parameters to the create_trainer function
    return redirect('/trainers')

# Update trainer
@app.route('/trainers/<int:trainer_id>', methods=['GET', 'POST'])
def edit_trainer(trainer_id):
    if request.method == 'POST':
        name = request.form.get('name')
        pokemon = request.form.get('pokemon')
        update_trainer(trainer_id, name, pokemon)
        return redirect('/trainers')

# Delete trainer
@app.route('/trainers/delete/<int:trainer_id>', methods=['POST'])
def delete(trainer_id):
    delete_trainer(trainer_id)
    return redirect('/trainers')


if __name__ == "__main__":
    app.run(debug=True)