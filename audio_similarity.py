import librosa
import numpy as np

# ================= EXTRACT AUDIO FEATURES =================
def extract_audio_features(video_path):
    try:
        y, sr = librosa.load(video_path, sr=None)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        return np.mean(mfcc, axis=1)
    except:
        return None


# ================= SIMILARITY =================
def compute_audio_similarity(video1, video2):

    f1 = extract_audio_features(video1)
    f2 = extract_audio_features(video2)

    if f1 is None or f2 is None:
        return 0

    # cosine similarity
    num = np.dot(f1, f2)
    den = (np.linalg.norm(f1) * np.linalg.norm(f2))

    if den == 0:
        return 0

    return float((num / den) * 100)