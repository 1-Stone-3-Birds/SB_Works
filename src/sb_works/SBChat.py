from kafka import KafkaProducer,KafkaConsumer
from json import loads
from datetime import datetime
import time
import threading
import json


def prochat():
    p = KafkaProducer(
        #TODO
        bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

    username = input("사용자 이름:")
    print("채팅 프로그램 - 메시지 발신자")
    print("메시지를 입력하세여.(종료시 'exit' 입력")

    while True:
        msg = input(f"{username}: ")
        if msg.lower() == 'exit':
            break
        if msg == "@이름변경":
            changename=input("변경할 이름:")
            username=changename
        data = {'message' : msg, 'time':time.time(), 'user': username}
        # TODO 보내기
        p.send('t3',value=data)
        p.flush()

def conchat():
    consumer = KafkaConsumer(
          't3',
          bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
          auto_offset_reset='latest',
          enable_auto_commit = True,

          value_deserializer=lambda x: loads(x.decode('utf-8'))
)


    print("채팅 프로그램 - 메시지 수신")
    print("메시지 대기 중 ....")

    try:
        for m in consumer:
            data= m.value
            print(f"[{data['user']}]:[{datetime.fromtimestamp(data['time'])}] {data['message']}")


    except KeyboardInterrupt:
        print("채팅 종료")
    finally:
        consumer.close()


# 스레드 생성
producer_thread = threading.Thread(target=prochat)
consumer_thread = threading.Thread(target=conchat)

# 스레드 시작
producer_thread.start()
consumer_thread.start()

# 스레드 종료 대기
producer_thread.join()
consumer_thread.join()
