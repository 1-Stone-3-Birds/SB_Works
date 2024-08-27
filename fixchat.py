from kafka import KafkaProducer,KafkaConsumer
from json import loads
from datetime import datetime
import time
import threading
import json
import sys
import os
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()
scheduler.start()

username = input("사용자 이름:")

def clear_screen():
    sys.stdout.write("\033[H\033[J")

messages = []




def prochat():
    global username 
    
    producer = KafkaProducer(
        bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
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
            
        if msg == "@이름변경":
            changename=input("변경할 이름:")
            changename_message = {"message" : f"{username}님이 {changename}으로 변경했습니다.","user":f"{changename}","time":time.time()}
            producer.send('chat3', value=changename_message)
            producer.flush()        
            username=changename
            continue

        data = {'message' : msg, 'time':time.time(), 'user': username}

        producer.send('chat3',value=data)
        producer.flush()

def conchat():
    global username
    consumer = KafkaConsumer(
          'chat3',
          bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
          #bootstrap_servers=["localhost:29092"],
          auto_offset_reset='latest',
          # auto_offset_reset='latest',
          enable_auto_commit = True,
          group_id = 'chat-group5',
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
