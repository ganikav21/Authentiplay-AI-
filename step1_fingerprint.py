import cv2
from skimage.metrics import structural_similarity as ssim

def extract_frames(video_path, skip=15):
    cap = cv2.VideoCapture(video_path)
    frames = []
    i = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if i % skip == 0:
            frames.append(frame)
        i += 1

    cap.release()
    return frames


def compare_ssim(f1, f2):
    f1 = cv2.resize(f1, (200, 200))
    f2 = cv2.resize(f2, (200, 200))

    g1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)

    score, _ = ssim(g1, g2, full=True)
    return score


def run_step1(video1, video2):
    v1_frames = extract_frames(video1)
    v2_frames = extract_frames(video2)

    matches = 0

    for f1 in v1_frames:
        best = 0
        for f2 in v2_frames:
            score = compare_ssim(f1, f2)
            best = max(best, score)

        if best > 0.75:
            matches += 1

    similarity = (matches / len(v1_frames)) * 100 if v1_frames else 0

    return {
        "matches": matches,
        "total_frames": len(v1_frames),
        "similarity": similarity
    }