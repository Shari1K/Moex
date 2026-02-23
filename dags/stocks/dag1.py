from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
import json
from datetime import datetime
from stocks.scripts.manager import fetch_data
from stocks.config import TICKERS

# BASE_DIR = os.path.dirname(__file__)
# CFG_PATH = os.path.join(BASE_DIR, "cfg.yaml")
#
#
# with open(CFG_PATH) as f:
#     config = yaml.safe_load(f)
#
# stocks = config["data"]["stock"]

default_args = {
    "owner": "airflow",
    # "depends_on_past": True,
    # "start_date": datetime(2026, 1, 1),
    # "end_date": datetime(2026, 1, 7),
    # "schedule": "@daily"
}

with DAG(
        dag_id="dag_moex",
        default_args=default_args,
        max_active_runs=1,
        # start_date=datetime(2025, 12, 1),
        # end_date=datetime(2025, 12, 3),
        start_date=datetime(2026, 1, 1),
        end_date=datetime(2026, 1, 5),
        schedule="0 0 * * 1-5"
) as dag:
    start = EmptyOperator(
        task_id=f"task_start")

    tasks = []
    for stock in TICKERS:
        task = PythonOperator(
            task_id=f"task_{stock}",
            python_callable=fetch_data,
            op_kwargs={"stock": stock}
        )
        tasks.append(task)

    end = EmptyOperator(
        task_id=f"task_end")

    start >> tasks >> end
