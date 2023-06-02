import requests

# Display all Pokemon
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
                    # Get the Pokemon name and capitalize it
                    "name": pokemon_data["name"].capitalize(),
                    # Get the URL of front sprite image
                    "image": pokemon_data["sprites"]["front_default"],
                    # Get the primary type of the Pokemon and capitalize it
                    "type": pokemon_data["types"][0]["type"]["name"].capitalize(),
                    "id": pokemon_data["id"]  # Get ID of the Pokemon
                }
                pokemon_list.append(pokemon)  # Append pokemon to pokemon_list

    return pokemon_list

# Pokemons details
def get_pokemon_details(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(url)

    if response.ok:
        data = response.json()
        pokemon = {
            "name": data["name"].capitalize(),
            "image": data["sprites"]["front_default"],
            # Get the height of the Pokemon and convert it from decimeters to meters
            "height": data["height"] / 10,
            # Get the weight of the Pokemon and convert it from hectograms to kilograms
            "weight": data["weight"] / 10,
            # Get the abilities of the Pokemon and capitalize them
            "abilities": [ability["ability"]["name"].capitalize() for ability in data["abilities"]],
            # Get the types of the Pokemon and capitalize them
            "types": [type_data["type"]["name"].capitalize() for type_data in data["types"]],
            # Get the weaknesses of the Pokemon
            "weaknesses": get_weaknesses(data["types"]),
            "stats": get_stats(data["stats"])  # Get the stats of the Pokemon
        }
        return pokemon

    return None

# Pokemons weakness
def get_weaknesses(types):
    weaknesses = set()
    for type_data in types:
        url = type_data["type"]["url"]
        response = requests.get(url)
        if response.ok:
            data = response.json()
            for damage_relation in data["damage_relations"]["double_damage_from"]:
                # Get the types that are weak against the Pokemon and capitalize them
                weaknesses.add(damage_relation["name"].capitalize())
    return list(weaknesses)

# Pokemons stats
def get_stats(stats):
    stat_names = ["hp", "attack", "defense", "speed"]
    # Get the base stats of the Pokemon for the specified stat names
    return {stat["stat"]["name"]: stat["base_stat"] for stat in stats if stat["stat"]["name"] in stat_names}
