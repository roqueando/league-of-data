from airflow.models.dag import DAG

with DAG("elt_base") as dag:
    print('starting dag')
