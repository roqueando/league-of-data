import urllib.request
import requests
from requests import RequestException
import os

LEAGUE_CHAMPIONS_URL = os.environ.get('LEAGUE_CHAMPIONS_URL')
LEAGUE_REALM = os.environ.get('LEAGUE_REALM')
LEAGUE_VERSIONS_URL = os.environ.get('LEAGUE_VERSIONS_URL')
LEAGUE_VERSIONS_URL_BUILT = f'{LEAGUE_VERSIONS_URL}/{LEAGUE_REALM}.json'


def get_versions() -> dict:
    """get the current version of league of legends"""
    print('aaaaaaaa')


def get_champions_json() -> dict:
    """
    Get all spells from API to ingest into a data lake
    """
    config = {
        'payload': {},
        'headers': {
            'Accept': 'application/json'
        }
    }
    urllib.request.urlretrieve(
        f"{LEAGUE_CHAMPIONS_URL}", "mp3.mp3")
    try:
        response = requests.get(f'{}/spells',
                                headers=config['headers'], data=config['payload'])
        data = response.json()
        return data
    except RequestException as e:
        raise SystemExit(e)
