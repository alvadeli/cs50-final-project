import requests

MUSICBRAINZ_API_URL = "https://musicbrainz.org/ws/2"
MUSICBRAINZ_RELEASE_GROUP = f"{MUSICBRAINZ_API_URL}/release-group"
MUSICBRAINZ_RELEASE = f"{MUSICBRAINZ_API_URL}/release"

def fetch_musicbrainz_data(query_params):
    query = "".join([f" AND {key}:{value}" for key, value in query_params.items()])
    url = f"{MUSICBRAINZ_RELEASE_GROUP}?query={query}&fmt=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["release-groups"]
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None  

def get_release_group(release_group_id):
    url = f"{MUSICBRAINZ_RELEASE_GROUP}/{release_group_id}?fmt=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None  
      
def get_album_cover_url(release_group_id):
    url = f"https://coverartarchive.org/release-group/{release_group_id}/front-250"
    try:
        response = requests.head(url)
        if response.status_code == 400:
            return None
        else:
            return url
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
