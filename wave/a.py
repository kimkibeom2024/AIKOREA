import librosa
import numpy as np
from scipy.spatial.distance import cosine

def extract_features(audio_path):
    # 오디오 로드 및 MFCC 특징 추출
    y, sr = librosa.load(audio_path)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc, axis=1)

def compare_audio_files(user_file, ref_file):
    # 두 오디오 파일의 MFCC 특징 추출
    user_features = extract_features(user_file)
    ref_features = extract_features(ref_file)
    
    # MFCC 유사도 계산 (발음 유사도)
    similarity = 1 - cosine(user_features, ref_features)
    return similarity * 100

def main():
    user_file = "C:\kb\wave\papago_audio\OREO.wav"
    ref_file = "C:\\kb\\wave\\audio\\OREO.wav"
    
    similarity = compare_audio_files(user_file, ref_file)
    print(f"\n발음 유사도 분석 결과:")
    print(f"사용자 발음 유사도: {similarity:.2f}%")

if __name__ == "__main__":
    main()