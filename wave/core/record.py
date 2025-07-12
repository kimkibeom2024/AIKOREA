import sounddevice as sd
import wave
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class AudioConfig:
    sample_rate: int = 48000  # 48kHz로 변경
    channels: int = 1
    dtype: str = 'int16'
    bit_depth: int = 2  # 16-bit

class AudioRecorder:
    def __init__(self, config: Optional[AudioConfig] = None):
        self.config = config or AudioConfig()
        self.recording = None
    
    def record(self, duration: int = 3) -> None:
        """지정된 시간동안 음성을 녹음합니다."""
        print("🎙️ 녹음 시작!")
        self.recording = sd.rec(
            int(duration * self.config.sample_rate),
            samplerate=self.config.sample_rate,
            channels=self.config.channels,
            dtype=self.config.dtype
        )
        sd.wait()
        print("✅ 녹음 완료!")
    
    def save(self, filename: str = "user/user_input.wav") -> str:
        """녹음된 음성을 파일로 저장합니다."""
        if self.recording is None:
            raise ValueError("녹음된 데이터가 없습니다. 먼저 record() 메소드를 호출하세요.")
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.config.channels)
            wf.setsampwidth(self.config.bit_depth)
            wf.setframerate(self.config.sample_rate)
            wf.writeframes(self.recording.tobytes())
        
        return filename

# 사용 예시
if __name__ == "__main__":
    recorder = AudioRecorder()
    recorder.record(duration=2.5)  # oreo.wav와 비슷한 길이로 녹음
    recorder.save("user/user_input.wav")