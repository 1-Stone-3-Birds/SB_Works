# 채팅로그가 남는 채팅방 


## 기능 
(1) 4명이 참여가능한 채팅 프로그램\
(2) 사용자 이름 받기 기능 \
(3) 이름변경 기능\
(4) exit로 나가기 기능 \
(5) 채팅 로그 저장\
(6) airflow로 로그 파일 parquet 파일 변환 기능 \
(7) 영화의 정보를 알려주는 영화 봇 기능\
(8) airflow dag 성공 및 실패를 채팅방에 알려주는 시스템 봇 기능 \
(9) 매일 오전 9시 25분에 스케줄 알림 메세지 전송하는 알림 봇 기능\


## 설치 환경 
- `python 3.8`이상
- `java`
```bash
sudo apt install java-17-openjdk
```
- `kafka-python`
```bash
pip install kafka-python
```
- `apscheduler`
```bash
pip install apscheduler
```
- 'pyproject.toml파일의 dependencies다운'
```bash
pdm install
```
- [Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/start.html)가 설치되어 있어야 합니다.
- [Apache Kafka](https://www.apache.org/dyn/closer.cgi?path=/kafka/3.8.0/kafka_2.13-3.8.0.tgz)가 설치되어 있어야 합니다.


* Airflow config 파일 dag 위치 환경설정
```bash
/home/centa/code/SB_Works/airflow/dags
```


## 설치 방법
1. 리포지토리를 클론
```bash
git clone https://github.com/asset-No-1/airflow_chat.git](https://github.com/1-Stone-3-Birds/SB_Works.git
```


## 프로그램 실행 방법
2. 프로그램 실행
```bash
python fixchat.py
```



## 프로그램 사용 방법 

#### 1. 그룹 아이디 입력

[그룹 아이디 설정 성공시]\
![image](https://github.com/user-attachments/assets/e3967b01-5c05-4511-8993-de99d5f556b1)

[그룹 아이디 설정 실패시]\
![image](https://github.com/user-attachments/assets/7de47395-8ecf-49ba-86fc-95b9ecbacb89)

#### 2. 사용자 이름 입력

![image](https://github.com/user-attachments/assets/9ac8f3ab-2f9d-47c5-ba39-f432406eafd1)

#### 3. 접속 완료 문구

![image](https://github.com/user-attachments/assets/66c3f2fb-158a-4b81-8ad3-59373c573cb8)

#### 4. 채팅작성

![image](https://github.com/user-attachments/assets/b035babd-a571-4e28-93f7-a8cf2681a3ec)

#### 5. 영화봇 기능

[영화봇 입력]\
![image](https://github.com/user-attachments/assets/c1276ea5-5026-4c41-9736-e7c288d31db1)

[영화봇 출력]\
![image](https://github.com/user-attachments/assets/9db3fef5-ba4e-493f-8955-c10e86ab97db)

[영화봇 입력 실패]\
![image](https://github.com/user-attachments/assets/d3316dc6-5b7d-45a1-9426-04036469e9bf)

#### 6. 시스템 봇 기능

[에어플로우 성공]\
![image](https://github.com/user-attachments/assets/d1c54ee0-3f06-4a11-944a-a24f3703d2c9)

[에어플로우 실패]\
![image](https://github.com/user-attachments/assets/b5d077b8-cfc8-46cb-ac38-2902d36a2ff9)

#### 7. 일정 봇 기능

![image](https://github.com/user-attachments/assets/fbb79c95-47d1-4293-bffc-52c461af3d7d)

#### 8. 도움말 봇 기능

![image](https://github.com/user-attachments/assets/3a72746e-7b43-407c-884c-b22a224de595)

#### 9. exit 프로그램 종료 

[입력]\
![image](https://github.com/user-attachments/assets/be381c8e-ccbd-4158-8cac-99455dfcff5b)

[상대방 채팅 로그에 보이는 퇴장 문구]\
![image](https://github.com/user-attachments/assets/f164fc0c-178c-4d95-a221-afad7c8880ea)

#### 10. 채팅로그 생성

![image](https://github.com/user-attachments/assets/3a9eb166-ac28-4eff-978e-e51febc934b3)

#### 11. 에어플로우로 로그파일 파퀘로 변환

![image](https://github.com/user-attachments/assets/dd20d799-0bea-48dc-bda9-279921f7b10c)
![image](https://github.com/user-attachments/assets/87e05409-13a0-41c3-9dd4-0093bb301c9e)
   
