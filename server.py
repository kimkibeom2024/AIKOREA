import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))  # 모든 IP에서 8080포트 사용
server_socket.listen(1)

print("서버가 준비되었습니다. 클라이언트를 기다리는 중...")

try:
    while True:
        conn, addr = server_socket.accept()  # 클라이언트 접속 대기
        print(f"연결됨: {addr}")

        try:
            while True:
                # 클라이언트로부터 데이터 수신
                data = conn.recv(1024).decode()
                
                if not data:  # 클라이언트가 연결을 종료한 경우
                    print("클라이언트가 연결을 종료했습니다.")
                    break
                
                print(f"클라이언트로부터 받은 데이터: {data}")

                # 클라이언트에 응답 보내기
                response = f"서버가 '{data}' 메시지를 성공적으로 받았습니다!"
                conn.send(response.encode())
                print(f"응답 전송: {response}")

        except Exception as e:
            print(f"클라이언트 통신 중 오류: {e}")
        finally:
            conn.close()  # 연결 종료
            print("클라이언트 연결이 종료되었습니다.")

except KeyboardInterrupt:
    print("\n서버를 종료합니다.")

finally:
    server_socket.close()
    print("서버가 완전히 종료되었습니다.")