# 채팅로그가 남는 채팅방 


## 기능 
(1) 4명이 참여가능한 채팅 프로그램\
(2) 사용자 이름 받기 기능 \
(3) 이름변경 기능\
(4) exit로 나가기 기능 \
(5) 채팅 로그 저장\
(6) airflow로 로그 파일 parquet 파일 변환 기능 \
(7) airflow dag 성공 및 실패시 채팅방 알림 기능 \

  
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
- 'pyproject.toml파일의 dependencies다운'
```bash
pdm install
```
- [Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/start.html)가 설치되어 있어야 합니다.
- [Apache Kafka](https://www.apache.org/dyn/closer.cgi?path=/kafka/3.8.0/kafka_2.13-3.8.0.tgz)가 설치되어 있어야 합니다.


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
사용하는 사람마다 그룹아이디 안겹치게 바꾸고 사용 

## 프로그램 사용 방법 

1. 사용자 이름 입력

![image](https://github.com/user-attachments/assets/9ac8f3ab-2f9d-47c5-ba39-f432406eafd1)

2. 채팅작성

![image](https://github.com/user-attachments/assets/533c29a4-2128-4279-82a4-037c014998d4)

3. 채팅로그 생성

![image](https://github.com/user-attachments/assets/3a9eb166-ac28-4eff-978e-e51febc934b3)

4. 에어플로우로 로그파일 파퀘로 변환

![image](https://github.com/user-attachments/assets/dd20d799-0bea-48dc-bda9-279921f7b10c)
![image](https://github.com/user-attachments/assets/87e05409-13a0-41c3-9dd4-0093bb301c9e)

   
5. exit 치면 나가기(제대로 구현안되서 exit 후에도 ctrl + c 로 강제종료 해야됨)

   
![image](https://github.com/user-attachments/assets/9a5835af-13dc-45f8-968d-d70a51d9859d)


