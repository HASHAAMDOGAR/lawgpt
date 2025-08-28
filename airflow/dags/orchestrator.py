import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta

sys.path.append('/opt/airflow/plugins')

def safe_main_callable():
    from insert_records import main
    return main()

default_args = {
    'description': 'A DAG to Orchestrator data',
    'start_date': datetime(2025, 1, 1),
    'catchup': False,
}

dag = DAG(
    dag_id='orchestrator_dag_1',
    default_args=default_args,
    schedule=timedelta(minutes=5),
)
with dag:
    task = PythonOperator(
        task_id='orchestrator_task',
        python_callable=safe_main_callable,
    )