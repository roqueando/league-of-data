from requests import RequestException
from botocore.exceptions import ClientError
from io import BytesIO
from datetime import datetime
import requests
import os
import boto3
import json
from trino.dbapi import connect
import pandas as pd

conn = connect(
    host=os.environ.get('TRINO_HOST'),
    port=os.environ.get('TRINO_PORT'),
    user=os.environ.get('TRINO_USER'),
    catalog=os.environ.get('TRINO_CATALOG'),
    schema=os.environ.get('TRINO_SCHEMA')
)

cursor = conn.cursor()

LEAGUE_LANG = os.environ.get('LEAGUE_LANG')
MINIO_URL = os.environ.get('MINIO_URL')
CURRENT_VERSION = os.environ.get('CURRENT_VERSION')

def get_object(s3, filename: str) -> dict:
    obj = s3.get_object(Bucket='league-data', Key=filename)
    return json.loads(obj['Body'].read())

def get_last_version():
    cursor.execute('select "n"."champion" as champion_version, inserted_at from minio.league_data.versions order by inserted_at desc')
    rows = cursor.fetchall()
    return rows[0]

def put_file(folder:str, filename: str, data: dict, s3) -> None:
    json_dumped = BytesIO(json.dumps(data).encode('utf-8'))
    s3.put_object(Bucket='league-data', Key=f'{folder}/{filename}.json', Body=json_dumped)

def transform():
    s3 = boto3.client('s3', endpoint_url=MINIO_URL,
                        config=boto3.session.Config(signature_version='s3v4'),
                        verify=False)
    champions = get_object(s3, "champions.json")
    df = pd.DataFrame(champions) \
        .drop(columns=['blurb', 'title', 'image', 'partype'])

    df['tags'] = df['tags'].apply(lambda x: x[0])

    df.loc[df['tags'] == 'Fighter', 'tags'] = 'JUNGLE'
    df.loc[df['tags'] == 'Tank', 'tags'] = 'TOP'
    df.loc[df['tags'] == 'Mage', 'tags'] = 'MID'
    df.loc[df['tags'] == 'Assassin', 'tags'] = 'BOT'
    df.loc[df['tags'] == 'Marksman', 'tags'] = 'BOT'
    df.loc[df['tags'] == 'Support', 'tags'] = 'SUP'

    for index, row in df.iterrows():
        filename = row['id']
        data_content = json.loads(row.to_json())
        put_file('champions', filename, data_content, s3)

    print('transformed data')

if __name__ == '__main__':
    transform()
