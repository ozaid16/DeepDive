import requests
import hashlib
import time

import pandas as pd


def generate_auth_params(public_key, private_key):
    timestamp = str(time.time())
    md5_hash = hashlib.md5(f"{timestamp}{private_key}{public_key}".encode("utf-8")).hexdigest()
    return {
        "apikey": public_key,
        "ts": timestamp,
        "hash": md5_hash,
    }

def fetch_marvel_characters(public_key, private_key):
    base_url = "https://gateway.marvel.com/v1/public/characters"
    auth_params = generate_auth_params(public_key, private_key)
    response = requests.get(base_url, params=auth_params)

    if response.status_code == 200:
        data = response.json()
        characters = data["data"]["results"]
        return characters
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []
    
if __name__ == "__main__":
    public_key = "acb2ae117474fc1e128f9862abbc5c74"
    private_key = "da21b0015a87d411335351136f4828edc2c76901"
    characters = fetch_marvel_characters(public_key, private_key)


ct=0
for character in characters:
        ct = ct+1
print(ct)

def fetch_marvel_charactersWithS(public_key, private_key, name_starts_with):
    base_url = "https://gateway.marvel.com/v1/public/characters"
    auth_params = generate_auth_params(public_key, private_key)
    params = {
        "nameStartsWith": name_starts_with,
    }
    response = requests.get(base_url, params={**auth_params, **params})

    if response.status_code == 200:
        data = response.json()
        characters = data["data"]["results"]
        return characters
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []
    
if __name__ == "__main__":
    public_key = "acb2ae117474fc1e128f9862abbc5c74"
    private_key = "da21b0015a87d411335351136f4828edc2c76901"
    name_starts_with = "S"

    characters = fetch_marvel_charactersWithS(public_key, private_key, name_starts_with)
    for character in characters:
        print(f"Name: {character['name']}, Description: {character['description']}")



def fetch_marvel_charactersWithLimit(public_key, private_key, limit=20):
    base_url = "https://gateway.marvel.com/v1/public/characters"
    auth_params = generate_auth_params(public_key, private_key)
    params = {
        "limit": limit,
    }
    response = requests.get(base_url, params={**auth_params, **params})

    if response.status_code == 200:
        data = response.json()
        characters = data["data"]["results"]
        return characters
    else:
        response.raise_for_status()  # Raise an exception for non-200 status codes


if __name__ == "__main__":
    public_key = "acb2ae117474fc1e128f9862abbc5c74"
    private_key = "da21b0015a87d411335351136f4828edc2c76901"
    total_characters = 500
    characters_per_request = 100
    characters = []

    try:
        for offset in range(0, total_characters, characters_per_request):
            characters += fetch_marvel_charactersWithLimit(public_key, private_key, characters_per_request)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

    # Convert the response to a pandas DataFrame
    if characters:
        df = pd.DataFrame(characters)

def fetch_marvel_characters(api_key, private_key, namestartswith=None, length=None):
    timestamp = str(int(time.time()))
    hash_value = hashlib.md5(f'{timestamp}{private_key}{api_key}'.encode()).hexdigest()
    base_url = 'https://gateway.marvel.com/v1/public/'
    endpoint = 'characters'
    params = {
        'apikey': api_key,
        'ts': timestamp,
        'hash': hash_value
    }
    if namestartswith:
        params['nameStartsWith'] = namestartswith
    if length:
        params['limit'] = length
    try:
        response = requests.get(f'{base_url}{endpoint}', params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        results = data['data']['results']
        return results
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"HTTP Error: {http_err}")
    except Exception as err:
        raise Exception(f"Error: {err}")
api_key = "acb2ae117474fc1e128f9862abbc5c74"
private_key = "da21b0015a87d411335351136f4828edc2c76901"
name_startswith = 'A'  # Optional parameter: Filter names starting with 'A'
length = 100  # Optional parameter: Set the number of results to fetch
try:
    characters = fetch_marvel_characters(api_key, private_key, name_startswith, length)
    print(f"Number of characters fetched: {len(characters)}")
except Exception as e:
    print(f"An error occurred: {e}")