import cv2
from skimage.metrics import structural_similarity as ssim


def compare_thumbnails(path1, path2):
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)

    if img1 is None or img2 is None:
        return 0.0

    img1 = cv2.resize(img1, (320, 180))
    img2 = cv2.resize(img2, (320, 180))

    g1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    score, _ = ssim(g1, g2, full=True)
    return round(max(0.0, score) * 100, 2)
