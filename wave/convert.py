from pydub import AudioSegment
from pydub.utils import mediainfo
import os

class AudioConverter:
    def __init__(self, input_dir="original_audio", output_dir="audio"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _sanitize_filename(self, filename):
        base_name = os.path.splitext(filename)[0]
        sanitized_base = base_name.replace(" ", "_")
        sanitized_filename = sanitized_base + os.path.splitext(filename)[1]
        return sanitized_base, sanitized_filename

    def _rename_if_needed(self, original_path, sanitized_path):
        if original_path != sanitized_path:
            os.rename(original_path, sanitized_path)
            print(f"🛠️  파일 이름 수정: {os.path.basename(original_path)} → {os.path.basename(sanitized_path)}")

    def _detect_format(self, filepath):
        try:
            info = mediainfo(filepath)
            return info.get("format_name")  # 예: 'mp3', 'aac', 'mov' 등
        except Exception as e:
            print(f"⚠️ 형식 감지 실패: {filepath} → {e}")
            return None

    def convert_audio_to_wav(self):
        for filename in os.listdir(self.input_dir):
            if filename.lower().endswith((".m4a", ".mp4", ".mp3")):
                original_path = os.path.join(self.input_dir, filename)
                sanitized_base, sanitized_filename = self._sanitize_filename(filename)
                sanitized_path = os.path.join(self.input_dir, sanitized_filename)
                self._rename_if_needed(original_path, sanitized_path)

                output_path = os.path.join(self.output_dir, sanitized_base + ".wav")
                print(f"🔄 변환 중: {sanitized_filename} → {sanitized_base}.wav")

                try:
                    file_format = self._detect_format(sanitized_path)
                    if not file_format:
                        raise ValueError("파일 형식을 감지할 수 없습니다.")

                    audio = AudioSegment.from_file(sanitized_path, format=file_format)
                    audio.export(output_path, format="wav")
                except Exception as e:
                    print(f"❌ 변환 실패: {sanitized_filename} → {e}")

        print(f"\n✅ 모든 변환 완료! 변환된 파일은 '{self.output_dir}'에 저장됨.")

# 실행 예시
if __name__ == '__main__':
    converter = AudioConverter(input_dir="papago", output_dir="papago_audio")
    converter.convert_audio_to_wav()
