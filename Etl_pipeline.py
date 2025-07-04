import os
import time
import chardet
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from config import  REM_TABLE, DATABASE_URL, csv_dir, TABLE_NAME, SCHEMA, NOT_NULL_COLUMNS, COLUMN_RENAME_MAP, DATE_COLUMNS, LOG_TABLE  # type: ignore



def extract_data(file_path):
    """Считывание CSV с автоматическим определением кодировки"""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding'] or 'utf-8'
    
    df = pd.read_csv(file_path, delimiter=';', encoding=encoding)
    return df.copy()

def transform_data(df, table_name):
    """Обработка данных для конкретной таблицы"""
    
    # Удаление дубликатов
    initial_count = len(df)
    df = df.drop_duplicates()

    # Замена значений на NULL
    null_values = ['', ' ', 'NULL', 'null', 'NaN', 'NA', 'N/A']
    df = df.replace(null_values, pd.NA)

    # Применение переименования колонок
    rename_map = COLUMN_RENAME_MAP.get(table_name, {})
    df = df.rename(columns=rename_map)
    
    # Приведение заголовков к нижнему регистру
    df.columns = [col.strip().lower() for col in df.columns]
    
    # Удаление строк с NULL в NOT NULL колонках
    not_null_cols = NOT_NULL_COLUMNS.get(table_name, [])
    for col in not_null_cols:
        col = col.lower()
        if col in df.columns:
            before = len(df)
            df = df.dropna(subset=[col])
            removed = before - len(df)
    
    # Преобразование дат
    date_cols = DATE_COLUMNS.get(table_name, {})
    for col, date_format in date_cols.items():
        col = col.lower()
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format=date_format, errors='coerce')
    return df

def load_data(engine, df, table_name, schema):
    """Загрузка данных в DB"""
    try:
        start_time = time.time()
        
        # Используем контекстный менеджер для транзакции
        with engine.begin() as conn:
            # Удаление данных из таблицы 
            if table_name == REM_TABLE:
                clear_sql = f"TRUNCATE TABLE {schema}.{table_name}"
                conn.execute(text(clear_sql))
            
            # Загрузка данных с заменой таблицы
            df.to_sql(
                name=table_name,
                con=conn,
                schema=schema,
                if_exists='replace',
                index=False
            )
        
        end_time = time.time()
        duration = end_time - start_time
        return True, duration, None
    
    except Exception as e:
        return False, 0, str(e)

def write_log(engine, log_data):
    """Запись данных в логовую таблицу"""
    # Используем контекстный менеджер для автоматического коммита
    with engine.begin() as conn:
        sql = text(f"""
            INSERT INTO {SCHEMA}.{LOG_TABLE} 
            (table_name, status, rows_loaded, start_time, end_time, duration, error_message)
            VALUES (:table_name, :status, :rows_loaded, :start_time, :end_time, :duration, :error_message)
            """)
        conn.execute(sql, log_data)
    return True

def main():
    """Основная функция выполнения ETL-процесса"""
    # Создание движка для подключения к БД
    engine = create_engine(DATABASE_URL)
    
    total_stats = []
    for table in TABLE_NAME:
        # Подготовка данных для лога
        log_data = {
            'table_name': table,
            'status': 'STARTED',
            'rows_loaded': 0,
            'start_time': datetime.now(),
            'end_time': None,
            'duration': None,
            'error_message': None
        }
        
        try:
            # Формирование пути к файлу
            csv_path = os.path.join(csv_dir, f"{table}.csv")
            
            # Проверка существования файла
            if not os.path.exists(csv_path):
                error_msg = f"File not found: {csv_path}"
                raise FileNotFoundError(error_msg)
                
            # EXTRACT
            raw_df = extract_data(csv_path)
            
            # TRANSFORM
            transformed_df = transform_data(raw_df, table)
            
            # LOAD
            success, load_duration, load_error = load_data(engine, transformed_df, table, SCHEMA)
            
            # Статистика выполнения
            status = "SUCCESS" if success else "FAILED"
            stats = {
                'table': table,
                'status': status,
                'start_file': csv_path,
                'rows_loaded': len(transformed_df),
                'load_time': f"{load_duration:.2f}s"
            }
            total_stats.append(stats)
            
            # Обновление данных для лога
            end_time = datetime.now()
            duration = end_time - log_data['start_time']
            
            log_data.update({
                'status': status,
                'rows_loaded': len(transformed_df),
                'end_time': end_time,
                'duration': str(duration),
                'error_message': load_error
            })
            
        except Exception as e:
            error_msg = str(e)
            total_stats.append({
                'table': table,
                'status': "FAILED",
                'error': error_msg
            })
            
            # Обновление данных для лога при ошибке
            log_data.update({
                'status': 'FAILED',
                'end_time': datetime.now(),
                'duration': str(datetime.now() - log_data['start_time']),
                'error_message': error_msg
            })
            
        finally:
            # Запись лога в БД
            write_log(engine, log_data)
    
    # Освобождение ресурсов БД
    engine.dispose()
    
if __name__ == "__main__":
    main()