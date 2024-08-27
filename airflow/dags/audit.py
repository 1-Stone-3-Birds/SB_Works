from airflow import DAG
from datetime import datetime, timedelta
from textwrap import dedent


from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import (
    PythonOperator,
    PythonVirtualenvOperator,
    BranchPythonOperator,
)

import os


with DAG(
    'multichat',
    default_args={
        'depends_on_past': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
    },
    description='multi chat DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 8, 25),
    #end_date=datetime(2015, 1, 5),
    catchup=True,
    tags=['spark'],
) as dag:


###################################################################

    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end', trigger_rule="all_done")

    def chk():
        curDir=os.getcwd()
        if os.path.exists(f"{curDir}/../../data"):
            return "rm.dir"
        else:
            return "save"

    def chkLog(ds_nodash):
        homePath=os.path.expanduser("~")
        print(f"{homePath}/code/SB_Works/logs/chat_{ds_nodash}.log")

        if os.path.isfile(f"{homePath}/code/SB_Works/logs/chat_{ds_nodash}.log"):
            return "check.parquet"
        
        return "send.rst"

    def sv(ds_nodash):
        import re
        import pandas as pd

        homePath=os.path.expanduser("~")

        with open(f"{homePath}/code/SB_Works/logs/chat_{ds_nodash}.log") as f:
            log_data=f.read()

        json_pattern = re.compile(r'{.*?}')
        json_matches = json_pattern.findall(log_data)
        _json=[]
        for j in json_matches:
            _json.append(eval(j))
        
        df=pd.DataFrame(_json)

        pattern = re.compile('[\w\s\!\@\#\$\%\&\(\)\~\*\-\=\+\_]')

        df["message"]=df["message"].apply(lambda x:"".join(pattern.findall(x)))
        df["user"]=df["user"].apply(lambda x:"".join(pattern.findall(x)))

        os.makedirs(f"{homePath}/code/SB_Works/parquet/", exist_ok=True)
        df.to_parquet(f"{homePath}/code/SB_Works/parquet/chat_{ds_nodash}.parquet")


    def send_rst():
        from kafka import KafkaProducer
        import time
        import threading
        import json

        def prochat():
            p = KafkaProducer(
                bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
                #bootstrap_servers=["localhost:29092"],
                value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )


            while True:
                data = {'message' : "task all success", 'time':time.time(), 'user': "AIRFLOW"}

                p.send('chat3',value=data)
                p.flush()

                raise KeyboardInterrupt
        # 스레드 생성
        producer_thread = threading.Thread(target=prochat)

        # 스레드 시작
        producer_thread.start()

        # 스레드 종료 대기
        producer_thread.join()


    check = BranchPythonOperator(
            task_id="check.parquet",
            python_callable=chk
    )

    rm_dir = BashOperator(
            task_id='rm.dir',
            bash_command="""
                rm ~/code/SB_Works/parquet/chat_{{ds_nodash}}.parquet
            """,
            )
    
    chkLog = BranchPythonOperator(
            task_id="chk.log.exist",
            python_callable=chkLog,
            )

    save = PythonOperator(
            task_id="save",
            python_callable=sv,
            trigger_rule="one_success"
            )

    send_rst=PythonVirtualenvOperator(
            task_id="send.rst",
            python_callable=send_rst,
            requirements=["kafka-python"],
            trigger_rule="none_failed"
            )
###################################################################

    start >> chkLog
    chkLog >> check >> rm_dir >> save >> send_rst  >> end
    chkLog >> send_rst
    check >> save
