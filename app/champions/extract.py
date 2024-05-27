import requests
from requests import RequestException
import os

LEAGUE_CHAMPIONS_URL = os.environ.get('LEAGUE_CHAMPIONS_URL')
LEAGUE_REALM = os.environ.get('LEAGUE_REALM')
LEAGUE_VERSIONS_URL = os.environ.get('LEAGUE_VERSIONS_URL')
LEAGUE_VERSIONS_URL_BUILT = f'{LEAGUE_VERSIONS_URL}/{LEAGUE_REALM}.json'
LEAGUE_LANG = os.environ.get('LEAGUE_LANG')


# TODO: versions need to be placed in minio for further analysis
def get_versions() -> dict:
    """get the current version of league of legends"""
    try:
        response = requests.get(LEAGUE_VERSIONS_URL_BUILD,
                                headers={'Accept': 'application/json'},
                                data={})
        return response.json
    except RequestException as e:
        raise SystemExit(e)


# TODO: champions need to be placed in minio for further analysis
def get_champions_json(versions: dict) -> dict:
    """
    Get all champions and save at minio
    """
    try:
        cdn = versions['cdn']
        champion_version = versions['n']['champion']
        url = f'{cdn}/{champion_version}/data/{LEAGUE_LANG}/champion.json'
        response = requests.get(url,
                                headers={'Accept': 'application/json'},
                                data={})
        data = response.json()
        return data
    except RequestException as e:
        raise SystemExit(e)

def extract():
    print('extracting...')

if __name__ == '__main__':
    extract()
