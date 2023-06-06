import requests

session = requests.Session()

# Display all Pokemon
def get_pokemon_list():
    pokemon_list = []
    url = "https://pokeapi.co/api/v2/pokemon?limit=151"

    try:
        response = session.get(url)
        response.raise_for_status()  # Raise an exception if the response status code is not successful
        results = response.json()["results"]

        for result in results:
            pokemon_url = result["url"]
            pokemon_response = session.get(pokemon_url)
            pokemon_data = pokemon_response.json()

            # Extract relevant data for each Pokemon and add it to the pokemon_list
            pokemon = {
                "name": pokemon_data["name"].capitalize(),
                "image": pokemon_data["sprites"]["front_default"],
                "type": pokemon_data["types"][0]["type"]["name"].capitalize(),
                "id": pokemon_data["id"]
            }
            pokemon_list.append(pokemon)

    except (requests.RequestException, ValueError) as e:
        print(f"An error occurred: {e}")

    return pokemon_list

# Get details of a specific Pokemon
def get_pokemon_details(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"

    try:
        response = session.get(url)
        response.raise_for_status()  # Raise an exception if the response status code is not successful
        data = response.json()

        # Extract detailed information about the Pokemon
        pokemon = {
            "name": data["name"].capitalize(),
            "image": data["sprites"]["front_default"],
            "height": data["height"] / 10,  # Convert height from decimeters to meters
            "weight": data["weight"] / 10,  # Convert weight from hectograms to kilograms
            "abilities": [ability["ability"]["name"].capitalize() for ability in data["abilities"]],
            "types": [type_data["type"]["name"].capitalize() for type_data in data["types"]],
            "weaknesses": get_weaknesses(data),  # Get the weaknesses of the Pokemon
            "stats": get_stats(data["stats"])  # Get the base stats of the Pokemon
        }
        return pokemon

    except (requests.RequestException, ValueError) as e:
        print(f"An error occurred: {e}")

    return None

# Get weaknesses of a Pokemon
def get_weaknesses(data):
    weaknesses = set()

    for type_data in data["types"]:
        if "damage_relations" in type_data["type"]:
            for damage_relation in type_data["type"]["damage_relations"]["double_damage_from"]:
                # Add types that are weak against the Pokemon to the weaknesses set
                weaknesses.add(damage_relation["name"].capitalize())

    return list(weaknesses)


# Get base stats of a Pokemon
def get_stats(stats):
    stat_names = ["hp", "attack", "defense", "speed"]

    # Extract the base stats for the specified stat names
    return {stat["stat"]["name"]: stat["base_stat"] for stat in stats if stat["stat"]["name"] in stat_names}
