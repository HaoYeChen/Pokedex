import aiohttp
import asyncio
import requests

pokemon_cache = {}


async def get_pokemon_data(url):
    if url in pokemon_cache:
        return pokemon_cache[url]

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                pokemon_data = await response.json()
                pokemon_cache[url] = pokemon_data
                return pokemon_data

    except (aiohttp.ClientError, ValueError) as e:
        print(f"An error occurred: {e}")
        return {}


async def get_pokemon_list():
    pokemon_list = []
    url = "https://pokeapi.co/api/v2/pokemon?limit=1000"

    try:
        response = requests.get(url)
        response.raise_for_status()
        results = response.json()["results"]

        pokemon_urls = [result["url"] for result in results]
        pokemon_data = await asyncio.gather(*[get_pokemon_data(url) for url in pokemon_urls])

        for data in pokemon_data:
            pokemon = {
                "name": data["name"].capitalize(),
                "image": data['sprites']['other']['official-artwork']['front_default'],
                "type": data["types"][0]["type"]["name"].capitalize(),
                "id": data["id"]
            }
            pokemon_list.append(pokemon)

    except (requests.RequestException, ValueError) as e:
        print(f"An error occurred: {e}")

    return pokemon_list


def get_pokemon_details(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"

    try:
        with requests.Session() as session:
            response = session.get(url)
            response.raise_for_status()
            data = response.json()

            pokemon = {
                "name": data["name"].capitalize(),
                "image": data['sprites']['other']['official-artwork']['front_default'],
                "height": data["height"] / 10,
                "weight": data["weight"] / 10,
                "abilities": [ability["ability"]["name"].capitalize() for ability in data["abilities"]],
                "types": [type_data["type"]["name"].capitalize() for type_data in data["types"]],
                "weaknesses": get_weaknesses(data),
                "stats": get_stats(data["stats"])
            }
            return pokemon

    except (requests.RequestException, ValueError) as e:
        print(f"An error occurred: {e}")

    return None


def get_weaknesses(data):
    weaknesses = set()

    for type_data in data["types"]:
        type_url = type_data["type"]["url"]

        try:
            with requests.Session() as session:
                type_response = session.get(type_url)
                type_response.raise_for_status()
                type_data = type_response.json()

                if "damage_relations" in type_data:
                    for damage_relation in type_data["damage_relations"]["double_damage_from"]:
                        weaknesses.add(damage_relation["name"].capitalize())

        except (requests.RequestException, ValueError) as e:
            print(f"An error occurred: {e}")

    return list(weaknesses)


def get_stats(stats):
    stat_names = ["hp", "attack", "defense", "speed"]
    return {stat["stat"]["name"]: stat["base_stat"] for stat in stats if stat["stat"]["name"] in stat_names}