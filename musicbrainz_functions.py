import requests


def fetch_musicbrainz_data(query_params):
    MUSICBRAINZ_API_URL = "https://musicbrainz.org/ws/2/release-group"
    query = "".join([f" AND {key}:{value}" for key, value in query_params.items()])
    url = f"{MUSICBRAINZ_API_URL}?query={query}&fmt=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["release-groups"]
    except requests.exceptions.RequestException as e:
        return None  

