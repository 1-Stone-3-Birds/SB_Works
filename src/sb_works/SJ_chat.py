from kafka import KafkaProducer,KafkaConsumer
from json import loads
from datetime import datetime
import time
import threading
import json
import sys
import os

username=input("사용자 입력:")

def clear_screen():
    sys.stdout.write("\033[H\033[J")

messages = []

def prochat():
    global username 
    p = KafkaProducer(
        bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
        #bootstrap_servers=["localhost:29092"],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
)


    while True:
        msg = input()
        if msg.lower() == 'exit':
            break
        if msg == "@이름변경":
            changename=input("변경할 이름:")
            username=changename
        data = {'message' : msg, 'time':time.time(), 'user': username}
        
        p.send('chat3',value=data)
        p.flush()

def conchat():
    global username
    consumer = KafkaConsumer(
          'chat3',
          bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
          #bootstrap_servers=["localhost:29092"],
          auto_offset_reset='latest',
          # auto_offset_reset='latest',
          enable_auto_commit = True,
          group_id = 'chat-group1',
          value_deserializer=lambda x: loads(x.decode('utf-8'))
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

#if __name__ == "__main__":
#    print("채팅 프로그램 - 메시지 발신 및 수신")
#    username = input("사용할 이름을 입력하세요 : ")

    # 스레드 생성
producer_thread = threading.Thread(target=prochat)
consumer_thread = threading.Thread(target=conchat)

    # 스레드 시작
producer_thread.start()
consumer_thread.start()

    # 스레드 종료 대기
producer_thread.join()
consumer_thread.join()
