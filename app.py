# from flask import Flask, render_template, request, redirect, url_for
# from service.user_service import register_user, login_user

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return redirect(url_for('login'))

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         register_user(username, password)
#         return redirect(url_for('login'))
#     else:
#         return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = login_user(username, password)
#         if user:
#             return render_template('welcome.html', username=user.username)
#         else:
#             return render_template('login.html', error='Invalid username or password')
#     else:
#         return render_template('login.html')

# if __name__ == '__main__':
#     app.run(debug=True)



# from flask import Flask, render_template, request, redirect, url_for
# import requests

# app = Flask(__name__)

# @app.route('/')
# def pokemon():
#     response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=151') # Fetch first 151 pokemon
#     pokemon_list = response.json()['results']
#     for pokemon in pokemon_list:
#         response = requests.get(pokemon['url'])
#         pokemon_data = response.json()
#         pokemon['image'] = pokemon_data['sprites']['front_default']
#     return render_template('index.html', pokemon_list=pokemon_list)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template
from services.pokemon_service import get_pokemon_list

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pokemon")
def pokemon():
    pokemon_list = get_pokemon_list()
    return render_template("pokemon.html", pokemon_list=pokemon_list)








if __name__ == "__main__":
    app.run(debug=True)