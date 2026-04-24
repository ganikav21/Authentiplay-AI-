import cv2
from skimage.metrics import structural_similarity as ssim

def compare_frame_sets(frames1, frames2):

    if len(frames1) == 0 or len(frames2) == 0:
        return 0

    matches = 0

    for f1 in frames1:
        f1 = cv2.resize(f1, (200, 200))
        g1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)

        best = 0

        for f2 in frames2:
            f2 = cv2.resize(f2, (200, 200))
            g2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)

            score, _ = ssim(g1, g2, full=True)
            best = max(best, score)

        if best > 0.7:
            matches += 1

    return (matches / len(frames1)) * 100