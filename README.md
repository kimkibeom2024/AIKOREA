# AIKOREA 소켓 서버

라즈베리파이에서 실행할 수 있는 Python 소켓 서버입니다.

## 라즈베리파이에서 설치 및 실행 방법

### 1. 저장소 클론하기

```bash
# 라즈베리파이 터미널에서 실행
git clone https://github.com/kimkibeom2024/AIKOREA.git
cd AIKOREA
```

### 2. Python 설치 확인

라즈베리파이에는 기본적으로 Python이 설치되어 있습니다. 버전을 확인해보세요:

```bash
python3 --version
```

### 3. 서버 실행하기

```bash
# 서버 실행
python3 server.py
```

서버가 성공적으로 시작되면 다음과 같은 메시지가 표시됩니다:
```
서버가 준비되었습니다. 클라이언트를 기다리는 중...
```

### 4. 서버 테스트하기

다른 컴퓨터에서 클라이언트를 실행하여 서버에 연결할 수 있습니다:

```python
# client.py 예시
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('라즈베리파이_IP주소', 8080))

# 메시지 전송
client_socket.send("안녕하세요!".encode())

# 서버 응답 수신
response = client_socket.recv(1024).decode()
print(f"서버 응답: {response}")

client_socket.close()
```

### 5. 방화벽 설정 (필요한 경우)

라즈베리파이에서 8080 포트를 열어야 할 수 있습니다:

```bash
# UFW 방화벽 사용 시
sudo ufw allow 8080

# 또는 iptables 사용 시
sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
```

### 6. 서버 백그라운드 실행

서버를 백그라운드에서 계속 실행하려면:

```bash
# nohup 사용
nohup python3 server.py &

# 또는 screen 사용
screen -S server
python3 server.py
# Ctrl+A, D로 screen 세션 분리
```

### 7. 서버 종료

```bash
# 프로세스 찾기
ps aux | grep server.py

# 프로세스 종료
kill [프로세스ID]
```

## 파일 구조

```
AIKOREA/
├── server.py      # 소켓 서버 코드
└── README.md      # 이 파일
```

## 주의사항

- 서버는 모든 IP 주소(0.0.0.0)에서 8080 포트로 연결을 받습니다
- 보안을 위해 프로덕션 환경에서는 방화벽 설정을 적절히 구성하세요
- 서버를 종료하려면 Ctrl+C를 누르세요

## 문제 해결

### 포트가 이미 사용 중인 경우
```bash
# 8080 포트 사용 중인 프로세스 확인
sudo netstat -tulpn | grep :8080

# 해당 프로세스 종료
sudo kill [프로세스ID]
```

### 권한 문제가 있는 경우
```bash
# 파일에 실행 권한 부여
chmod +x server.py
```

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 