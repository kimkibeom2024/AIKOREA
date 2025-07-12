import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))  # 모든 IP에서 8080포트 사용
server_socket.listen(1)

print("서버가 준비되었습니다. 클라이언트를 기다리는 중...")

try:
    while True:
        conn, addr = server_socket.accept()  # 클라이언트 접속 대기
        print(f"연결됨: {addr}")

        data = conn.recv(1024).decode()  # 데이터 수신
        print(f"클라이언트로부터 받은 데이터: {data}")

        # 클라이언트에 응답 보내기
        conn.send("메시지를 성공적으로 받았습니다!".encode())

        conn.close()  # 연결 종료

except KeyboardInterrupt:
    print("서버를 종료합니다.")

finally:
    server_socket.close()