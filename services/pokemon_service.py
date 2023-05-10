import requests

def get_pokemon_list():
    pokemon_list = []
    url = "https://pokeapi.co/api/v2/pokemon?limit=151"
    response = requests.get(url)

    if response.ok:
        results = response.json()["results"]
        for result in results:
            pokemon_url = result["url"]
            pokemon_response = requests.get(pokemon_url)

            if pokemon_response.ok:
                pokemon_data = pokemon_response.json()
                pokemon = {
                    "name": pokemon_data["name"].capitalize(),
                    "image": pokemon_data["sprites"]["front_default"],
                    "type": pokemon_data["types"][0]["type"]["name"].capitalize(),
                    "id": pokemon_data["id"]
                }
                pokemon_list.append(pokemon)

    return pokemon_list