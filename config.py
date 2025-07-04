DATABASE_URL = "postgresql+psycopg2://airflow:airflow@postgres:5432/postgres"

csv_dir = '/data/csv'

TABLE_NAME = ['ft_balance_f',
              'ft_posting_f',
              'md_account_d',
              'md_currency_d',
              'md_exchange_rate_d',
              'md_ledger_account_s']

SCHEMA = "ds"

LOG_TABLE = "etl_log"

REM_TABLE = 'ft_posting_f'
# Колонки, которые не могут содержать NULL значения
NOT_NULL_COLUMNS = {
    "ft_balance_f": [
        "on_date",
        "account_rk"
        ],
    "ft_posting_f": [
        "oper_date", 
        "credit_account_rk", 
        "debet_account_rk"
        ],
    "md_account_d": [
        "data_actual_date",
        "data_actual_end_date",
        "account_rk",
        "account_number",
        "char_type",
        "currency_rk",
        "currency_code"
    ],
    "md_currency_d": [
        "currency_rk", 
        "data_actual_date"
        ],
    "md_exchange_rate_d": [
        "data_actual_date", 
        "currency_rk"
        ],
    "md_ledger_account_s": [
        "ledger_account", 
        "start_date"
        ]
}

# Маппинг для переименования колонок (старое_имя: новое_имя)
COLUMN_RENAME_MAP = {
  "ft_balance_f": {
    "ON_DATE": "on_date",
    "ACCOUNT_RK": "account_rk",
    "CURRENCY_RK": "currency_rk",
    "BALANCE_OUT": "balance_out"
  },
  "ft_posting_f": {
    'OPER_DATE':'oper_date',
    'CREDIT_ACCOUNT_RK':'credit_account_rk',
    'DEBET_ACCOUNT_RK':'debet_account_rk',
    'CREDIT_AMOUNT':'credit_amount',
    'DEBET_AMOUNT':'debet_amount'
      },
  "md_account_d": {
    "DATA_ACTUAL_DATE": "data_actual_date",
    "DATA_ACTUAL_END_DATE": "data_actual_end_date",
    "ACCOUNT_RK": "account_rk",
    "ACCOUNT_NUMBER": "account_number",
    "CHAR_TYPE": "char_type",
    "CURRENCY_RK": "currency_rk",
    "CURRENCY_CODE": "currency_code"
  },
  "md_currency_d": {
    "CURRENCY_RK": "currency_rk",
    "DATA_ACTUAL_DATE": "data_actual_date",
    "DATA_ACTUAL_END_DATE": "data_actual_end_date",
    "CURRENCY_CODE": "currency_code",
    "CODE_ISO_CHAR": "code_iso_char"
  },
  "md_exchange_rate_d": {
    "DATA_ACTUAL_DATE": "data_actual_date",
    "DATA_ACTUAL_END_DATE": "data_actual_end_date",
    "CURRENCY_RK": "currency_rk",
    "REDUCED_COURCE": "reduced_course",
    "CODE_ISO_NUM": "code_iso_num"
  },
  "md_ledger_account_s": {
    "CHAPTER": "chapter",
    "CHAPTER_NAME": "chapter_name",
    "SECTION_NUMBER": "section_number",
    "SECTION_NAME": "section_name",
    "SUBSECTION_NAME": "subsection_name",
    "LEDGER1_ACCOUNT": "ledger1_account",
    "LEDGER1_ACCOUNT_NAME": "ledger1_account_name",
    "LEDGER_ACCOUNT": "ledger_account",
    "LEDGER_ACCOUNT_NAME": "ledger_account_name",
    "CHARACTERISTIC": "characteristic",
    "START_DATE": "start_date",
    "END_DATE": "end_date"
  }
}

# Колонки, которые нужно преобразовать в дату
DATE_COLUMNS = {
    "ft_balance_f": {
        "on_date": "%d.%m.%Y"  
    },
    "ft_posting_f": {
        "oper_date": "%d-%m-%Y"  
    },
    "md_account_d": {
        "data_actual_date": "%Y-%m-%d",  
        "data_actual_end_date": "%Y-%m-%d"
    },
    "md_currency_d": {
        "data_actual_date": "%Y-%m-%d",
        "data_actual_end_date": "%Y-%m-%d"
    },
    "md_exchange_rate_d": {
        "data_actual_date": "%Y-%m-%d",
        "data_actual_end_date": "%Y-%m-%d"
    },
    "md_ledger_account_s": {
        "start_date": "%Y-%m-%d",
        "end_date": "%Y-%m-%d"
    }
}