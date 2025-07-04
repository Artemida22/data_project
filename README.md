data_project/
├── data/                   
│   └── csv/                  # CSV файлы для загрузки
├── dags/                     # DAG-файлы Airflow
│   ├── etl_project/          # Python-модули ETL
│   │   ├── __init__.py
│   │   ├── Etl_pipeline.py
│   │   └── config.py
│   └── manual_etl_dag.py
├── docker-compose.yml        # Docker Compose конфигурация
├── requirements.txt          # Зависимости Python
