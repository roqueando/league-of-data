from requests import RequestException
from botocore.exceptions import ClientError
from io import BytesIO
from datetime import datetime
import requests
import os
import boto3
import json
import sys

LEAGUE_REALM = os.environ.get('LEAGUE_REALM')
LEAGUE_VERSIONS_URL = os.environ.get('LEAGUE_VERSIONS_URL')
LEAGUE_VERSIONS_URL_BUILT = f'{LEAGUE_VERSIONS_URL}/{LEAGUE_REALM}.json'
LEAGUE_LANG = os.environ.get('LEAGUE_LANG')
MINIO_URL = os.environ.get('MINIO_URL')
MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY')


def get_versions() -> dict:
    """get the current version of league of legends"""
    try:
        response = requests.get(LEAGUE_VERSIONS_URL_BUILT,
                                headers={'Accept': 'application/json'},
                                data={})
        return response.json()
    except RequestException as e:
        raise SystemExit(e)


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


def put_file_at_root(filename: str, data: dict, s3) -> None:
    json_dumped = BytesIO(json.dumps(data).encode('utf-8'))
    s3.Bucket('league-data').put_object(Key=f'{filename}.json', Body=json_dumped)

def put_file(folder:str, filename: str, data: dict, s3) -> None:
    json_dumped = BytesIO(json.dumps(data).encode('utf-8'))
    s3.Bucket('league-data').put_object(Key=f'{folder}/{filename}.json', Body=json_dumped)

def extract():
    s3 = boto3.resource('s3', endpoint_url=MINIO_URL,
                        config=boto3.session.Config(signature_version='s3v4'),
                        aws_access_key_id=MINIO_ACCESS_KEY,
                        aws_secret_access_key=MINIO_SECRET_KEY,
                        verify=False)
    try:
        filename = datetime.now().strftime("%Y-%m-%d")
        versions = get_versions()
        versions['inserted_at'] = filename

        put_file('versions', filename, versions, s3)
        print('versions saved!')

        champions = get_champions_json(versions)
        champions_list = []
        for _, champ_data in champions['data'].items():
            champions_list.append(champ_data)

        put_file_at_root('champions', champions_list, s3)
        print('extracted!')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    extract()
