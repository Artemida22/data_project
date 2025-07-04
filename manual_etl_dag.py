from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Правильное добавление пути к модулям
current_dir = os.path.dirname(os.path.abspath(__file__))
etl_project_dir = os.path.join(current_dir, "etl_project")
sys.path.insert(0, etl_project_dir)

# Импорт функций после добавления пути
from Etl_pipeline import main

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG(
    'manual_etl_pipeline',
    default_args=default_args,
    description='Запуск ETL-пайплайна по требованию',
    schedule_interval=None,
    catchup=False,
    tags=['manual', 'etl'],
    
)

def run_etl():
    """Обертка для запуска основной ETL-функции"""
    main()

run_etl_task = PythonOperator(
    task_id='execute_etl_pipeline',
    python_callable=run_etl,
    dag=dag,
)