import socket
import time
from YB_Pcb_Car import YB_Pcb_Car

# 로봇 카 제어 객체 초기화
try:
    car = YB_Pcb_Car()
    print("로봇 카 제어 초기화 성공")
except Exception as e:
    print(f"로봇 카 제어 초기화 실패: {e}")
    car = None

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

                # 명령 처리
                if data == "FORWARD":
                    if car:
                        try:
                            print("🚗 로봇 전진 시작!")
                            car.Car_Run(50, 50)  # 좌우 바퀴 속도 50으로 전진
                            time.sleep(2)  # 2초간 전진
                            car.Car_Stop()  # 정지
                            print("🛑 로봇 정지!")
                            response = "FORWARD_SUCCESS"
                        except Exception as e:
                            print(f"로봇 제어 오류: {e}")
                            response = "FORWARD_ERROR"
                    else:
                        response = "ROBOT_NOT_AVAILABLE"
                else:
                    # 기타 메시지에 대한 기본 응답
                    response = f"서버가 '{data}' 메시지를 성공적으로 받았습니다!"

                # 클라이언트에 응답 보내기
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
    # 로봇 정지
    if car:
        try:
            car.Car_Stop()
            print("로봇을 정지시켰습니다.")
        except:
            pass
    
    server_socket.close()
    print("서버가 완전히 종료되었습니다.")