import requests

session = requests.Session()


pokemon_cache = {}

# Display all Pokemon
def get_pokemon_list():
    pokemon_list = []
    url = "https://pokeapi.co/api/v2/pokemon?limit=151"

    try:
        response = requests.get(url)
        # Raise an exception if the response status code is not successful
        response.raise_for_status()
        results = response.json()["results"]

        for result in results:
            pokemon_data = get_pokemon_data(result["url"])

            # Extract relevant data for each Pokemon and add it to the pokemon_list
            pokemon = {
                "name": pokemon_data["name"].capitalize(),
                "image": pokemon_data['sprites']['other']['official-artwork']['front_default'],
                "type": pokemon_data["types"][0]["type"]["name"].capitalize(),
                "id": pokemon_data["id"]
            }
            pokemon_list.append(pokemon)

    except (requests.RequestException, ValueError) as e:
        print(f"An error occurred: {e}")

    return pokemon_list


def get_pokemon_data(url):
    if url in pokemon_cache:
        return pokemon_cache[url]

    try:
        response = requests.get(url)
        # Raise an exception if the response status code is not successful
        response.raise_for_status()
        pokemon_data = response.json()
        pokemon_cache[url] = pokemon_data  # Cache the fetched Pokemon data
        return pokemon_data

    except (requests.RequestException, ValueError) as e:
        print(f"An error occurred: {e}")
        return {}


pokemon_list = get_pokemon_list()

# Get details of a specific Pokemon
def get_pokemon_details(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"

    try:
        response = session.get(url)
        # Raise an exception if the response status code is not successful
        response.raise_for_status()
        data = response.json()

        # Extract detailed information about the Pokemon
        pokemon = {
            "name": data["name"].capitalize(),
            "image": data['sprites']['other']['official-artwork']['front_default'],
            # Convert height from decimeters to meters
            "height": data["height"] / 10,
            # Convert weight from hectograms to kilograms
            "weight": data["weight"] / 10,
            "abilities": [ability["ability"]["name"].capitalize() for ability in data["abilities"]],
            "types": [type_data["type"]["name"].capitalize() for type_data in data["types"]],
            # Get the weaknesses of the Pokemon
            "weaknesses": get_weaknesses(data),
            # Get the base stats of the Pokemon
            "stats": get_stats(data["stats"])
        }
        return pokemon

    except (requests.RequestException, ValueError) as e:
        print(f"An error occurred: {e}")

    return None

# Get weaknesses of a Pokemon
def get_weaknesses(data):
    weaknesses = set()

    for type_data in data["types"]:
        type_url = type_data["type"]["url"]
        type_response = session.get(type_url)
        type_data = type_response.json()

        if "damage_relations" in type_data:
            for damage_relation in type_data["damage_relations"]["double_damage_from"]:
                # Add types that are weak against the Pokemon to the weaknesses set
                weaknesses.add(damage_relation["name"].capitalize())

    return list(weaknesses)


# Get base stats of a Pokemon
def get_stats(stats):
    stat_names = ["hp", "attack", "defense", "speed"]

    # Extract the base stats for the specified stat names
    return {stat["stat"]["name"]: stat["base_stat"] for stat in stats if stat["stat"]["name"] in stat_names}
