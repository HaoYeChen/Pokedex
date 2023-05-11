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
                    "name": pokemon_data["name"].capitalize(),
                    "image": pokemon_data["sprites"]["front_default"],
                    "type": pokemon_data["types"][0]["type"]["name"].capitalize(),
                    "id": pokemon_data["id"]
                }
                pokemon_list.append(pokemon)

    return pokemon_list

def get_pokemon_details(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(url)

    if response.ok:
        data = response.json()
        pokemon = {
            "name": data["name"].capitalize(),
            "image": data["sprites"]["front_default"],
            "height": data["height"] / 10,  # Convert decimeters to meters
            "weight": data["weight"] / 10,  # Convert hectograms to kilograms
            "abilities": [ability["ability"]["name"].capitalize() for ability in data["abilities"]],
            # "gender": get_gender_ratio(data["gender_rate"]),
            "types": [type_data["type"]["name"].capitalize() for type_data in data["types"]],
            "weaknesses": get_weaknesses(data["types"]),
            "stats": get_stats(data["stats"]),
            "evolutions": get_evolutions(data["species"]["url"])
        }
        return pokemon

    return None

# def get_gender_ratio(gender_rate):
#     if gender_rate is None:
#         return "Genderless"
#     elif gender_rate == -1:
#         return "Genderless"
#     elif gender_rate == 0:
#         return "Male"
#     elif gender_rate == 8:
#         return "Female"
#     else:
#         return f"Male: {8 - gender_rate}/8, Female: {gender_rate}/8"

def get_weaknesses(types):
    weaknesses = set()
    for type_data in types:
        url = type_data["type"]["url"]
        response = requests.get(url)
        if response.ok:
            data = response.json()
            for damage_relation in data["damage_relations"]["double_damage_from"]:
                weaknesses.add(damage_relation["name"].capitalize())
    return list(weaknesses)

def get_stats(stats):
    stat_names = ["hp", "attack", "defense", "special_attack", "special_defense", "speed"]
    return {stat["stat"]["name"]: stat["base_stat"] for stat in stats if stat["stat"]["name"] in stat_names}

def get_evolutions(url):
    response = requests.get(url)

    if response.ok:
        data = response.json()
        evolutions = []
        while "evolves_to" in data and len(data["evolves_to"]) > 0:
            evolution_data = data["evolves_to"][0]
            evolution = evolution_data["species"]["name"].capitalize()
            evolutions.append(evolution)
            data = evolution_data
        return evolutions

    return []

def get_evolutions(url):
    response = requests.get(url)

    if response.ok:
        data = response.json()
        evolutions = []
        evolution_chain = data["evolution_chain"]["url"]
        response = requests.get(evolution_chain)

        if response.ok:
            data = response.json()
            chain = data["chain"]

            while "evolves_to" in chain and len(chain["evolves_to"]) > 0:
                evolution = chain["evolves_to"][0]["species"]["name"].capitalize()
                evolutions.append(evolution)
                chain = chain["evolves_to"][0]

        return evolutions

    return []