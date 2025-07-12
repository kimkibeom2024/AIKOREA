import librosa
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
from sklearn.preprocessing import StandardScaler
import os

def normalize_audio(y):
    """
    음성 신호를 -1 ~ 1 범위로 정규화
    """
    return y / np.max(np.abs(y))

def get_scaled_mfcc(audio_path, n_mfcc=13):
    """오디오 파일에서 MFCC 특성을 추출하고 정규화합니다."""
    y, sr = librosa.load(audio_path, sr=None)
    
    # 음성 정규화
    y = librosa.util.normalize(y)
    
    # 묵음 제거
    y_trimmed, _ = librosa.effects.trim(y, top_db=20)
    
    # MFCC 추출 (파라미터 조정)
    mfcc = librosa.feature.mfcc(
        y=y_trimmed, 
        sr=sr,
        n_mfcc=n_mfcc,
        n_fft=2048,
        hop_length=512,
        n_mels=40,  # mel 밴드 수 증가
        fmin=20,    # 최소 주파수
        fmax=8000   # 최대 주파수
    )
    
    # 델타 특성 추가
    delta_mfcc = librosa.feature.delta(mfcc)
    delta2_mfcc = librosa.feature.delta(mfcc, order=2)
    
    # 특성 결합
    features = np.concatenate([mfcc, delta_mfcc, delta2_mfcc])
    
    # 정규화
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    return features_scaled.T

def compare_audio(reference_path, user_path, scale_factor=10):
    """
    두 MFCC를 비교하고 유사도 점수(0~100) 반환
    """
    try:
        ref = get_scaled_mfcc(reference_path)
        user = get_scaled_mfcc(user_path)
        
        # DTW 거리 계산
        distance, path = fastdtw(ref, user, dist=euclidean)
        
        # 경로 길이로 정규화된 거리 계산
        path_length = len(path)
        normalized_distance = distance / path_length
        
        # 점수 계산 방식 개선
        base_score = 100 * np.exp(-normalized_distance / scale_factor)
        
        # 길이 페널티 계산
        length_ratio = min(len(ref), len(user)) / max(len(ref), len(user))
        length_penalty = length_ratio ** 0.5  # 제곱근으로 페널티 완화
        
        # 최종 점수 계산
        final_score = base_score * length_penalty
        
        # 점수 범위 제한
        score = max(0, min(100, final_score))
        
        print(f"🎙️ 발음 비교 결과:")
        print(f"📊 Raw Distance: {distance:.2f}")
        print(f"📏 Normalized Distance: {normalized_distance:.2f}")
        print(f"📐 Length Ratio: {length_ratio:.2f}")
        print(f"💯 Final Score: {score:.2f}%")
        
        return round(score, 2)
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return 0

# 테스트용 코드
if __name__ == "__main__":
    ref_path = os.path.join("audio", "pringles.wav")
    user_path = os.path.join("user", "user_input.wav")
    score = compare_audio(ref_path, user_path)
    print(f"테스트 점수: {score}%")