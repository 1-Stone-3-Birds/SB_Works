from kafka import KafkaProducer,KafkaConsumer
from json import loads
from datetime import datetime
import time
import threading
import json
import sys
import os
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import re


while True:
    group_id = input("사용자 그룹: ")
    usercheck=os.system(f"$KAFKA_HOME/bin/kafka-consumer-groups.sh --bootstrap-server ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092 --list | grep '^{group_id}$'")
    if usercheck==0:
        print("이미 존재하는 사용자 그룹입니다 다른 이름을 입력해주세요")
        continue
    else:  
        username = input("사용자 이름:")
        pattern =  re.compile('[\w\s\!\@\#\$\%\&\(\)\~\*\-\=\+\_]')
        matches = pattern.findall(username)
        username="".join(matches)
        break

scheduler = BackgroundScheduler()
scheduler.start()
messages = []

#movie_data = pd.read_parquet('/SB_Works/data')
home_dir = os.path.expanduser('~')
movie_data = pd.read_parquet(f"{home_dir}/code/SB_Works/data/parquet")

def clear_screen():
    sys.stdout.write("\033[H\033[J")

def prochat():
    global username 
    global group_id
    producer = KafkaProducer(
        bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
        #bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('latin')
    )
    enter_message = {
            "chat_room": "chat3",
            "message": f"{username}님이 입장하셨습니다.",
            "user":f"{username}",
            "time":time.time()
        }
    producer.send('chat3',value=enter_message)
    producer.flush()

    #alert 함수
    def send_alert():
        # 매일 정각 9시 25분에 호출되는 알림 함수
        alert_message = {
            "chat_room": "chat3",
            "message": "에자일 칸반 미팅 5분 전입니다!",
	        "user":"@알림봇",
	        "time":time.time()
        }
        producer.send('chat3', value=alert_message)
        producer.flush()

    scheduler.add_job(send_alert, 'cron', hour=9, minute=25)
    # scheduler.add_job(send_alert, 'cron', hour=16, minute=30)
    
    while True:
        msg=input()
        # clear_screen()
        if msg.lower() == 'exit':
            exit_message = {"message" : f"{username}님이 퇴장했습니다...","user":f"{username}","time":time.time()}
            producer.send('chat3', value=exit_message)
            producer.flush()
            os._exit(1)  
            
        if msg == "@도움말":
            helpMsg="""
            ------ help -----------------------------------------
            | 1. 영화정보를 조회하고 싶면으시면: @영화봇        |
            | 2. 대화명을 변경하고 싶으시면: @이름변경          |
            | 3. 대화를 종료하고 싶으시면: exit                 |
            -----------------------------------------------------
              계속 하시려면 Enter를 입력해주세요 ...
            """
            print(helpMsg)
            continue            


        if msg == "@영화봇":
            # 영화 제목을 입력받기
            moviename = input("영화제목 : ")
            df = movie_data[movie_data['movieNm'] == moviename]

            if not df.empty:
                directors = df['directors'].values[0]
                openDt = df['openDt'].values[0]
                nationAlt = df['nationAlt'].values[0]
                message = f"{moviename}(은)는 {nationAlt}에서 {openDt}일에 개봉한 '{directors}'감독의 영화입니다."
                data = {'message': message, 'time': time.time(), 'user': '영화봇'}
                producer.send('chat3', value=data)
                producer.flush()
                continue 
            else:
                print("해당 영화 정보를 찾을 수 없습니다.")
                print("계속하시려면 Enter를 입력해주세요.")
                continue


        if msg == "@이름변경":
            changename=input("변경할 이름:")
            changename_message = {"message" : f"{username}님이 {changename}으로 변경했습니다.","user":f"{changename}","time":time.time()}
            producer.send('chat3', value=changename_message)
            producer.flush()        
            username=changename
            continue

        ##### 글자 깨짐 미표출
        pattern = re.compile('[\w\s\!\@\#\$\%\&\(\)\~\*\-\=\+\_]')
        matches = pattern.findall(msg)

        msg="".join(matches)
        #####

        data = {'message' : msg, 'time':time.time(), 'user': username}

        producer.send('chat3',value=data)
        producer.flush()

def conchat():
    global username
    global group_id
    consumer = KafkaConsumer(
          'chat3',
          bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
          #bootstrap_servers=["localhost:9092"],
          auto_offset_reset='latest',
          # auto_offset_reset='latest',
          enable_auto_commit = True,
          group_id = f'{group_id}',
          value_deserializer=lambda x: loads(x.decode('latin'))
)


    try:
        for m in consumer:
            data= m.value
            timeparse=datetime.fromtimestamp(data['time'])
            messages.append(f"[{data['user']}]:[{str(timeparse)}] {data['message']}")
            clear_screen()
            ## data["time"]=str(timeparse)  ####
            for message in messages: 
                print(message)
            
            sys.stdout.write(f"{username}:")
            sys.stdout.flush()    
                
            ###################################
            timeparse=datetime.fromtimestamp(data['time'])
            curDir=os.getcwd()
            os.makedirs(f"{curDir}/logs", exist_ok=True)
            with open(f"{curDir}/logs/chat_{timeparse.strftime('%Y%m%d')}.log","a") as f:
                data["time"]=str(timeparse)
                data["offset"]=m.offset
                f.write(str(data))
                f.write("\n")
            ###################################

    except KeyboardInterrupt:
        print("채팅 종료")
    finally:
        consumer.close()

# if __name__ == "__main__":
# print("채팅 프로그램 - 메시지 발신 및 수신")
# username = input("사용할 이름을 입력하세요 : ")
# 스케줄러 설정

# 스레드 생성
producer_thread = threading.Thread(target=prochat)
consumer_thread = threading.Thread(target=conchat)

# 스레드 시작
producer_thread.start()
consumer_thread.start()

# 스레드 종료 대기
producer_thread.join()
consumer_thread.join()

#    try:
#        while True:
#            time.sleep(1)  # 스케줄러가 계속 실행되도록 유지
#    except (KeyboardInterrupt, SystemExit):
