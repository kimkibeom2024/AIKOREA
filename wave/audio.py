import wave
import numpy as np
from pydub import AudioSegment
from typing import Tuple

class AudioAnalyzer:
    @staticmethod
    def get_audio_info(file_path: str) -> dict:
        """웨이브 파일의 기본 정보를 반환합니다."""
        with wave.open(file_path, 'rb') as wf:
            return {
                'channels': wf.getnchannels(),
                'sample_width': wf.getsampwidth(),
                'frame_rate': wf.getframerate(),
                'frames': wf.getnframes(),
                'duration': wf.getnframes() / wf.getframerate()
            }
    
    @staticmethod
    def normalize_audio(file_path: str, target_db: float = -20.0) -> AudioSegment:
        """오디오 파일을 로드하고 정규화합니다."""
        audio = AudioSegment.from_wav(file_path)
        
        # 볼륨 정규화
        change_in_db = target_db - audio.dBFS
        normalized_audio = audio.apply_gain(change_in_db)
        
        return normalized_audio
    
    @staticmethod
    def prepare_files_for_comparison(file1: str, file2: str) -> Tuple[AudioSegment, AudioSegment]:
        """두 오디오 파일을 비교를 위해 준비합니다."""
        # 두 파일을 동일한 설정으로 정규화
        audio1 = AudioAnalyzer.normalize_audio(file1)
        audio2 = AudioAnalyzer.normalize_audio(file2)
        
        # 동일한 샘플링 레이트로 변환
        target_sample_rate = 16000
        if audio1.frame_rate != target_sample_rate:
            audio1 = audio1.set_frame_rate(target_sample_rate)
        if audio2.frame_rate != target_sample_rate:
            audio2 = audio2.set_frame_rate(target_sample_rate)
        
        # 모노로 변환
        if audio1.channels > 1:
            audio1 = audio1.set_channels(1)
        if audio2.channels > 1:
            audio2 = audio2.set_channels(1)
        
        return audio1, audio2

    @staticmethod
    def compare_files(file1: str, file2: str) -> dict:
        """두 오디오 파일의 특성을 비교합니다."""
        info1 = AudioAnalyzer.get_audio_info(file1)
        info2 = AudioAnalyzer.get_audio_info(file2)
        
        print("\n[파일 비교 결과]")
        print(f"\n파일1: {file1}")
        print(f"- 채널: {info1['channels']}")
        print(f"- 샘플레이트: {info1['frame_rate']}Hz")
        print(f"- 비트심도: {info1['sample_width'] * 8}bit")
        print(f"- 길이: {info1['duration']:.2f}초")
        
        print(f"\n파일2: {file2}")
        print(f"- 채널: {info2['channels']}")
        print(f"- 샘플레이트: {info2['frame_rate']}Hz")
        print(f"- 비트심도: {info2['sample_width'] * 8}bit")
        print(f"- 길이: {info2['duration']:.2f}초")
        
        return {
            'file1': info1,
            'file2': info2
        }

# 사용 예시
if __name__ == "__main__":
    analyzer = AudioAnalyzer()
    
    # 파일 경로 설정
    user_file = "papago_audio/oreo.wav"
    reference_file = "audio/oreo.wav"
    
    # 파일 특성 비교
    comparison = analyzer.compare_files(user_file, reference_file)
    
    # 정규화된 파일 준비
    normalized_user, normalized_ref = analyzer.prepare_files_for_comparison(user_file, reference_file)