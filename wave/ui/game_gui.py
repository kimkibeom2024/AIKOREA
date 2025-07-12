import os
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

from ui.custom_widgets import HoverableImageLabel
from core.compare import compare_audio
from core.record import AudioRecorder, AudioConfig

WORDS = ["OREO", "Coca_Cola", "KFC", "McDonald", "Nutella", "Pringles", "SNICKERS", "Starbucks"]
AUDIO_DIR = "audio"
USER_AUDIO = "user/user_input.wav"
IMAGE_DIR = "images"
PASS_THRESHOLD = 60
RECORD_SECONDS = 3

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

        self.show_image(WORDS[0])

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
