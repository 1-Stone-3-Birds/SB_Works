from airflow import DAG
from datetime import datetime, timedelta
from textwrap import dedent

# Operators; we need this to operate!

from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import (
    ExternalPythonOperator,
    PythonOperator,
    PythonVirtualenvOperator,
    is_venv_installed,
    PythonVirtualenvOperator,
    BranchPythonOperator,
)

with DAG(
    'multichat',
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
    },
    description='multi chat DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2015, 1, 1),
    #end_date=datetime(2015, 1, 5),
    catchup=True,
    tags=['spark'],
) as dag:


###################################################################

    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end', trigger_rule="all_done")


    check = BashOperator(
            task_id="check",
            bash_command="bash {{ var.value.CHECK_SH }} {{ds_nodash}}"
#            echo "check"
#            DONE_PATH=~/data/done/{{ds_nodash}}
#            DONE_PATH_FILE="${DONE_PATH}/_DONE"
#
#            #파일 존재 여부 확인
#            if [ -e "$DONE_PATH_FILE" ]; then
#                figlet "Let's move on"
#                exit 0
#            else
#                echo "I'll be back => $DONE_PATH_FILE"
#                exit 1
#            fi
    )

    rm_dir = BashOperator(
            task_id='rm.dir',
            bash_command='rm -rf ~/tmp/test_parquet/load_dt={{ ds_nodash }}',
            )

    save = BashOperator(
            task_id='save',
            bash_command="""
            """
    )

###################################################################

    start >> [check, rm_dir] >> save >> end
