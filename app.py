from flask import Flask, render_template, abort, request, redirect, flash, url_for
import asyncio
from services.pokemon_service import get_pokemon_list
from services.pokemon_service import get_pokemon_details

app = Flask(__name__)

'''
pokedex page
'''
@app.route("/")
def index():
    pokemon_list = asyncio.run(get_pokemon_list())
    return render_template("pokedex.html", pokemon_list=pokemon_list)

'''
pokemon details page
'''
@app.route("/<pokemon_id>")
def pokemon_details(pokemon_id):
    # Convert pokemon_id to an integer
    pokemon_id = int(pokemon_id)

    # Fetch the details of the specific Pokemon using the ID
    pokemon = get_pokemon_details(pokemon_id)

    if pokemon is None:
        # Handle the case if the Pokemon is not found
        abort(404)

    # Fetch the IDs of the previous and next Pokemon
    prev_pokemon_id = pokemon_id - 1 if pokemon_id > 1 else None
    next_pokemon_id = pokemon_id + 1 if pokemon_id < 151 else None

    return render_template("pokemon_details.html", pokemon=pokemon, prev_pokemon_id=prev_pokemon_id, next_pokemon_id=next_pokemon_id)

'''
search on pokemon details page
'''
@app.route("/pokedex", methods=["GET", "POST"])
def pokemon_search():
    if request.method == "POST":
        search_query = request.form.get("search")
        if search_query:
            # Search for the Pokemon by name or ID
            try:
                pokemon_id = int(search_query)
                return redirect(url_for("pokemon_details", pokemon_id=pokemon_id))
            except ValueError:
                pokemon_list = get_pokemon_list()
                for pokemon in pokemon_list:
                    if pokemon["name"].lower() == search_query.lower():
                        return redirect(url_for("pokemon_details", pokemon_id=pokemon["id"]))
                flash("Pokemon not found.")

    return redirect(url_for("pokemon_list"))



'''
404 page
'''
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)