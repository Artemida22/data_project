CREATE SCHEMA IF NOT EXISTS ds;
create table if NOT exists  DS.FT_BALANCE_F (
on_date DATE not null,
account_rk NUMERIC not null,
currency_rk NUMERIC,
balance_out FLOAT,
PRIMARY KEY (on_date, account_rk)
);
create table if NOT exists  DS.FT_POSTING_F (
oper_date DATE not null,
credit_account_rk NUMERIC not null,
debet_account_rk NUMERIC not null,
credit_amount FLOAT,
debet_amount FLOAT
);
create table if NOT exists  DS.MD_ACCOUNT_D  (
data_actual_date DATE not null,
data_actual_end_date DATE not null,
account_rk NUMERIC not null,
account_NUMERIC VARCHAR(20) not null,
char_type VARCHAR(1) not null,
currency_rk NUMERIC not null,
currency_code VARCHAR(3) not null,
PRIMARY key (DATA_ACTUAL_DATE, ACCOUNT_RK)
);
create table if NOT exists  DS.MD_CURRENCY_D(
currency_rk NUMERIC not null,
data_actual_date DATE not null,
data_actual_end_date DATE,
currency_code VARCHAR(3),
code_iso_char VARCHAR(3),
PRIMARY key (CURRENCY_RK, DATA_ACTUAL_DATE)
);
create table if NOT exists DS.MD_EXCHANGE_RATE_D  (
data_actual_date DATE not null,
data_actual_end_date DATE,
currency_rk NUMERIC not null,
reduced_cource FLOAT,
code_iso_num VARCHAR(3),
PRIMARY KEY (DATA_ACTUAL_DATE, CURRENCY_RK)
);
create table if NOT exists DS.MD_LEDGER_ACCOUNT_S (
chapter CHAR(1),
chapter_name VARCHAR(16),
section_number INTEGER,
section_name VARCHAR(22),
subsection_name VARCHAR(21),
ledger1_account INTEGER,
ledger1_account_name VARCHAR(47),
ledger_account INTEGER not null,
ledger_account_name VARCHAR(153),
characteristic CHAR(1),
is_resident INTEGER,
is_reserve INTEGER,
is_reserved INTEGER,
is_loan INTEGER,
is_reserved_assets INTEGER,
is_overdue INTEGER,
is_interest INTEGER,
pair_account VARCHAR(5),
start_date DATE not null,
end_date DATE,
is_rub_only INTEGER,
min_term VARCHAR(1),
min_term_measure VARCHAR(1),
max_term VARCHAR(1),
max_term_measure VARCHAR(1),
ledger_acc_full_name_translit VARCHAR(1),
is_revaluation VARCHAR(1),
is_correct VARCHAR(1),
primary key (LEDGER_ACCOUNT, START_DATE)
);
CREATE TABLE IF NOT EXISTS DS.etl_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    rows_loaded INTEGER,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    duration VARCHAR(50),
    error_message TEXT
);