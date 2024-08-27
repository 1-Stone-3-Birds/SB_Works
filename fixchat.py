from kafka import KafkaProducer,KafkaConsumer
from json import loads
from datetime import datetime
import time
import threading
import json
import sys
import os
from apscheduler.schedulers.background import BackgroundScheduler


p = KafkaProducer(
    bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
    #bootstrap_servers=["localhost:29092"],
    value_serializer=lambda x: json.dumps(x).encode('latin')
)



def get_director(movie_title):
    home_dir = os.path.expanduser('~')   
    json_file_path = os.path.join(f"{home_dir}/code/SB_Works/data/movies/year=2015/data.json")
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as file:
            movie_data = json.load(file)
            for movie in movie_data:
                if movie['movieNm'] == movie_title:
                    directors = movie.get('directors', [])
                    if directors:
                        director_names = [director['peopleNm'] for director in directors]
                        return ", ".join(director_names)
                    else:
                        return "감독 정보가 없습니다."
    return "영화 정보를 찾을 수 없습니다."

#alert 함수
def send_alert():
    # 매일 정각 9시 25분에 호출되는 알림 함수
    alert_message = {
        "chat_room": "chat3",
        "message": "에자일 칸반 미팅 5분 전입니다!",
	    "user":"@알림봇",
	    "time":time.time()
    }
    p.send('chat3', value=alert_message)
    p.flush()


def clear_screen():
    sys.stdout.write("\033[H\033[J")

messages = []

def prochat():
    global username 


    while True:
        # clear_screen()
        msg = input(f"{username}: ")
        if msg.lower() == 'exit':
            break
        if msg == "@이름변경":
            changename=input("변경할 이름:")
            username=changename
        data = {'message' : msg, 'time':time.time(), 'user': username}
        if msg.startswith("@챗봇"):
           command, *query = msg.split(" ", 1)
           if command == "@챗봇":
               if query:
                   movie_title = query[0]
                   director_info = get_director(movie_title)
                   msg = f"{movie_title}의 감독은 {director_info}입니다."
               else:
                   msg = "영화 제목을 입력해주세요."

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

if __name__ == "__main__":
    print("채팅 프로그램 - 메시지 발신 및 수신")
    username = input("사용할 이름을 입력하세요 : ")
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

    try:
        while True:
            time.sleep(1)  # 스케줄러가 계속 실행되도록 유지
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()  # 프로그램 종료 시 스케줄러 정리
        producer_thread.join()
        consumer_thread.join()
    # 스레드 종료 대기
#     producer_thread.join()
#    consumer_thread.join()
