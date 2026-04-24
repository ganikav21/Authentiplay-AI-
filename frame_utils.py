import cv2

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