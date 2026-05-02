from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime
from stocks.scripts.manager import data_to_PostgreSQL, data_to_ClickHouse
from stocks.config import TICKERS


default_args = {
    "owner": "airflow",
}


with DAG(
        dag_id="dag_moex",
        default_args=default_args,
        max_active_runs=1,
        start_date=datetime(2026, 1, 1),
        end_date=datetime(2026, 4, 28),
        schedule="0 0 * * 1-5",
        catchup=True
) as dag:
    start = EmptyOperator(
        task_id=f"task_start")

    load_to_pg = []
    for stock in TICKERS:
        unload = PythonOperator(
            task_id=f"task_{stock}",
            python_callable=data_to_PostgreSQL,
            op_kwargs={"stock": stock}
        )
        load_to_pg.append(unload)

    load_to_click = PythonOperator(
        task_id=f"task_load_to_click",
        python_callable=data_to_ClickHouse,
    )

    end = EmptyOperator(
        task_id=f"task_end")

    start >> load_to_pg >> load_to_click >>end