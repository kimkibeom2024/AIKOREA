import librosa
import numpy as np
import os
from scipy.spatial.distance import cosine

class AudioComparator:
    def __init__(self, user_audio_dir=None, papago_audio_dir=None):
        self.user_audio_dir = user_audio_dir
        self.papago_audio_dir = papago_audio_dir

    def extract_features(self, audio_path):
        # 오디오 로드 및 MFCC 특징 추출
        y, sr = librosa.load(audio_path)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        return np.mean(mfcc, axis=1)

    def compare_audio_files(self, file1, file2):
        # 두 오디오 파일의 MFCC 특징 추출
        features1 = self.extract_features(file1)
        features2 = self.extract_features(file2)
        
        # MFCC 유사도 계산 (발음 유사도)
        similarity = 1 - cosine(features1, features2)
        return similarity * 100

    def compare_all_files(self):
        if not self.user_audio_dir or not self.papago_audio_dir:
            raise ValueError("디렉토리 경로가 설정되지 않았습니다.")
        
        results = []
        
        for user_file in os.listdir(self.user_audio_dir):
            if user_file.endswith('.wav'):
                papago_file = os.path.join(self.papago_audio_dir, user_file)
                user_file_path = os.path.join(self.user_audio_dir, user_file)
                
                if os.path.exists(papago_file):
                    similarity = self.compare_audio_files(user_file_path, papago_file)
                    results.append({
                        'file_name': user_file,
                        'similarity': similarity
                    })
        
        return results

def main():
    comparator = AudioComparator(
        user_audio_dir="C:\\kb\\wave\\audio",
        papago_audio_dir="C:\\kb\\wave\\papago_audio"
    )
    
    # 특정 파일 비교
    file1 = "C:\\kb\\wave\\audio\\oreo.wav"
    file2 = "C:\\kb\\wave\\user\\user_input.wav"
    similarity = comparator.compare_audio_files(file1, file2)
    print(f"\n파일1: {file1}와 파일2: {file2}의 발음 유사도: {similarity:.2f}%")
    
    # 모든 파일 비교
    results = comparator.compare_all_files()
    
    # 결과 출력
    for result in results:
        print(f"\n파일 분석: {result['file_name']}")
        print(f"발음 유사도: {result['similarity']:.2f}%")

if __name__ == "__main__":
    main()
