import cv2
from step1_fingerprint import extract_frames, compare_ssim

orb = cv2.ORB_create()


def orb_match(f1, f2):
    g1 = cv2.cvtColor(cv2.resize(f1, (200, 200)), cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(cv2.resize(f2, (200, 200)), cv2.COLOR_BGR2GRAY)

    kp1, des1 = orb.detectAndCompute(g1, None)
    kp2, des2 = orb.detectAndCompute(g2, None)

    if des1 is None or des2 is None:
        return 0

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    return len(matches)


def run_step2(video1, video2):
    v1_frames = extract_frames(video1)
    v2_frames = extract_frames(video2)

    matches = 0

    for f1 in v1_frames:
        best_score = 0

        for f2 in v2_frames:
            ssim_score = compare_ssim(f1, f2)
            orb_score = orb_match(f1, f2) / 50

            combined = max(ssim_score, orb_score)
            best_score = max(best_score, combined)

        if best_score > 0.75:
            matches += 1

    similarity = (matches / len(v1_frames)) * 100 if v1_frames else 0

    return {
        "matches": matches,
        "total_frames": len(v1_frames),
        "similarity": similarity
    }