from kafka import KafkaProducer,KafkaConsumer
from json import dumps, loads
from datetime import datetime
import time
import threading
import json

from apscheduler.schedulers.background import BackgroundScheduler

# Kafka 프로듀서 설정
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def send_alert():
    # 매일 정각 9시 25분에 호출되는 알림 함수
    alert_message = {
        "chat_room": "nth1",
        "message": "에자일 칸반 미팅 5분 전입니다!",
	"user":"@알림봇",
	"time":time.time()
    }
    producer.send('nth1', value=alert_message)
    producer.flush()
   

def prochat():
    # 채팅 프로그램 - 메시지 발신

    p = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    username = input("사용자 이름: ")
    print("채팅 프로그램 - 메시지 발신자")
    print("메시지를 입력하세여.(종료시 'exit' 입력)")

    while True:
        msg = input(f"{username}: ")
        if msg.lower() == 'exit':
            break
        if msg == "@이름변경":
            changename = input("변경할 이름: ")
            username = changename
        data = {'message': msg, 'time': time.time(), 'user': username}
        p.send('nth1', value=data)
        p.flush()

def conchat():
    # 채팅 프로그램 - 메시지 수신
    consumer = KafkaConsumer(
        'nth1',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print("채팅 프로그램 - 메시지 수신")
    print("메시지 대기 중 ....")

    try:
        for m in consumer:
            data = m.value
            print(f"[{data['user']}]:[{datetime.fromtimestamp(data['time'])}] {data['message']}")

    except KeyboardInterrupt:
        print("채팅 종료")
    finally:
        consumer.close()

if __name__ == "__main__":
    # 스케줄러 설정
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_alert, 'cron', hour=9, minute=25)
    scheduler.start()

    # 스레드 생성
    producer_thread = threading.Thread(target=prochat)
    consumer_thread = threading.Thread(target=conchat)

    # 스레드 시작
    producer_thread.start()
    consumer_thread.start()

    # 스레드 종료 대기
    try:
        while True:
            time.sleep(1)  # 스케줄러가 계속 실행되도록 유지
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()  # 프로그램 종료 시 스케줄러 정리
        producer_thread.join()
        consumer_thread.join()
<<<<<<< HEAD

=======
>>>>>>> v0.2.0/audit
