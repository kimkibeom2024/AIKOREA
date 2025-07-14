import os
import numpy as np
import socket
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

from ui.custom_widgets import HoverableImageLabel
from core.compare import compare_audio
from core.record import AudioRecorder, AudioConfig
from pydub import AudioSegment
from pydub.playback import play

WORDS = ["OREO", "Coca_Cola", "KFC", "McDonald", "Nutella", "Pringles", "SNICKERS", "Starbucks"]
AUDIO_DIR = "audio"
USER_AUDIO = "user/user_input.wav"
IMAGE_DIR = "images"
PASS_THRESHOLD = 40
RECORD_SECONDS = 3

# 라즈베리파이 서버 설정
RASPBERRY_PI_IP = '10.150.57.246'  # 라즈베리파이 IP 주소
RASPBERRY_PI_PORT = 8080

class PronunciationGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎙 발음 게임")
        self.setFixedSize(720, 750)

        # QSS 적용
        with open("ui/style.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.index = 0
        self.recorder = AudioRecorder(AudioConfig())  # 기본 설정으로 AudioRecorder 초기화

        # 레이아웃
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # 이미지
        self.image_label = HoverableImageLabel()
        self.image_label.setCursor(Qt.PointingHandCursor)
        self.image_label.mousePressEvent = self.start_recording
        self.layout.addWidget(self.image_label)

        # 볼륨 바
        self.volume_container = QFrame()
        self.volume_container.setObjectName("volume_container")
        self.volume_container.setFixedHeight(12)
        self.layout.addWidget(self.volume_container)

        self.volume_bar = QFrame(self.volume_container)
        self.volume_bar.setObjectName("volume_bar")
        self.volume_bar.setGeometry(0, 0, 0, 12)

        self.recording_timer = QTimer()
        self.recording_timer.timeout.connect(self.update_volume_bar)
        self.recording_timer.setInterval(100)

        # TCP 클라이언트 소켓 초기화
        self.client_socket = None
        self.connect_to_raspberry_pi()

        self.show_image(WORDS[0])

    def connect_to_raspberry_pi(self):
        """라즈베리파이 서버에 연결"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((RASPBERRY_PI_IP, RASPBERRY_PI_PORT))
            print(f"라즈베리파이 서버에 연결되었습니다: {RASPBERRY_PI_IP}:{RASPBERRY_PI_PORT}")
        except Exception as e:
            print(f"라즈베리파이 서버 연결 실패: {e}")
            self.client_socket = None

    def send_forward_signal(self):
        """라즈베리파이로 전진 신호 전송"""
        if self.client_socket:
            try:
                message = "FORWARD"
                self.client_socket.send(message.encode())
                response = self.client_socket.recv(1024).decode()
                print(f"라즈베리파이 응답: {response}")
            except Exception as e:
                print(f"라즈베리파이 통신 오류: {e}")
                # 연결 재시도
                self.connect_to_raspberry_pi()

    def resizeEvent(self, event):
        if self.index < len(WORDS):
            self.show_image(WORDS[self.index])
        super().resizeEvent(event)

    def show_image(self, word):
        image_path = os.path.join(IMAGE_DIR, f"{word}.png")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            scaled = pixmap.scaled(
                self.width(),
                int(self.height() * 0.85),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)

    def start_recording(self, event):
        self.volume_bar.setFixedWidth(0)
        self.recorder.record(duration=RECORD_SECONDS)
        self.recorder.save(USER_AUDIO)
        self.compare_current_word()

    def update_volume_bar(self):
        if hasattr(self.recorder, 'recording') and self.recorder.recording is not None:
            volume = np.linalg.norm(self.recorder.recording) * 10
            bar_width = max(1, min(int(volume * 3), self.width()))
            self.volume_bar.setFixedWidth(bar_width)

    def compare_current_word(self):
        if self.index >= len(WORDS):
            QMessageBox.information(self, "🎉 완료", "모든 단어를 성공했습니다!")
            self.close()
            return

        word = WORDS[self.index]
        ref_path = os.path.join(AUDIO_DIR, f"{word}.wav")
        score = compare_audio(ref_path, USER_AUDIO)

        if score >= PASS_THRESHOLD:
            # 정답 음성 재생
            try:
                import winsound
                winsound.PlaySound(ref_path, winsound.SND_FILENAME)
            except Exception as e:
                print(f"정답 음성 재생 오류: {e}")
            
            # 라즈베리파이로 전진 신호 전송
            self.send_forward_signal()
            
            self.index += 1
            if self.index < len(WORDS):
                self.show_image(WORDS[self.index])
            else:
                QMessageBox.information(self, "🎉 완료", "모든 단어를 성공했습니다!")
                self.close()
        else:
            self.flash_fail()

    def flash_fail(self):
        self.setStyleSheet("QWidget { background-color: #ffe6e6; }")
        QTimer.singleShot(300, self.restore_style)

    def restore_style(self):
        with open("ui/style.qss", "r") as f:
            self.setStyleSheet(f.read())

    def closeEvent(self, event):
        """프로그램 종료 시 소켓 정리"""
        if self.client_socket:
            try:
                self.client_socket.close()
                print("라즈베리파이 서버 연결이 종료되었습니다.")
            except:
                pass
        event.accept()
