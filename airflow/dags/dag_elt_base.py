from airflow.models.dag import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.models import Variable
from datetime import timedelta

with DAG(
    "elt_champions",
    default_args={
        'depends_on_past': False,
        'email': ['vitor.roquep@gmail.com'],
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1)
    },
    description="The ELT for champions"
) as dag:
    LEAGUE_REALM = Variable.get('LEAGUE_REALM')
    LEAGUE_LANG = Variable.get('LEAGUE_LANG')
    LEAGUE_VERSIONS_URL = Variable.get('LEAGUE_VERSIONS_URL')
    LEAGUE_VERSIONS_URL_BUILT = f'{LEAGUE_VERSIONS_URL}/{LEAGUE_REALM}.json'
    LEAGUE_LANG = Variable.get('LEAGUE_LANG')
    TRINO_HOST = Variable.get('TRINO_HOST')
    TRINO_PORT = Variable.get('TRINO_PORT')
    TRINO_USER = Variable.get('TRINO_USER')
    TRINO_CATALOG = Variable.get('TRINO_CATALOG')
    TRINO_SCHEMA = Variable.get('TRINO_SCHEMA')
    minio_access_key = Variable.get("MINIO_ACCESS_KEY")
    minio_secret_key = Variable.get("MINIO_SECRET_KEY")
    minio_url = Variable.get("MINIO_URL")
    environment = {
        'LEAGUE_VERSIONS_URL': LEAGUE_VERSIONS_URL,
        'LEAGUE_REALM': LEAGUE_REALM,
        'LEAGUE_LANG': LEAGUE_LANG,
        'MINIO_ACCESS_KEY': minio_access_key,
        'MINIO_SECRET_KEY': minio_secret_key,
        'MINIO_URL': minio_url,
        'TRINO_HOST': TRINO_HOST,
        'TRINO_PORT': TRINO_PORT,
        'TRINO_USER': TRINO_USER,
        'TRINO_CATALOG': TRINO_CATALOG,
        'TRINO_SCHEMA': TRINO_SCHEMA
    }
    network = 'league-of-data_trino-network'

    extract_task = DockerOperator(
        task_id='extract_champions',
        image='roqueando/app:stable',
        container_name='champions_extract',
        docker_url='unix://var/run/docker.sock',
        api_version='auto',
        xcom_all=False,
        auto_remove=True,
        command="champions.extract",
        environment=environment,
        network_mode=network
    )

    transform_task = DockerOperator(
        task_id='transform_champions',
        image='roqueando/app:stable',
        container_name='champions_transform',
        docker_url='unix://var/run/docker.sock',
        api_version='auto',
        xcom_all=False,
        auto_remove=True,
        command="champions.transform",
        environment=environment,
        network_mode=network
    )

    extract_task >> transform_task

