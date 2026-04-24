import cv2
from frame_hash import extract_frames, compute_hashes, compare_hashes
from thumbnail_similarity import compare_thumbnails

from audio_similarity import compute_audio_similarity

try:
    from clip_similarity import compute_clip_similarity
    from clip_explainer import explain_clip
    CLIP_AVAILABLE = True
except:
    CLIP_AVAILABLE = False

from evidence_panel import compute_frame_match_timeline, get_evidence_frames
from propagation_model import generate_propagation


def get_duration(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.release()

    if fps == 0:
        return 0
    return int(frames / fps)


def run_pipeline(video1_path, video2_path, thumb1=None, thumb2=None):

    frames1 = extract_frames(video1_path)
    frames2 = extract_frames(video2_path)

    hashes1 = compute_hashes(frames1)
    hashes2 = compute_hashes(frames2)

    frame_similarity = compare_hashes(hashes1, hashes2)

    thumb_similarity = 0
    if thumb1 and thumb2:
        try:
            thumb_similarity = compare_thumbnails(thumb1, thumb2)
        except:
            pass

    clip_sim = 0
    clip_explanation = {}

    if CLIP_AVAILABLE:
        try:
            clip_sim = compute_clip_similarity(video1_path, video2_path)
            clip_explanation = explain_clip(video1_path, video2_path)
        except:
            pass

    try:
        audio_sim = compute_audio_similarity(video1_path, video2_path)
    except:
        audio_sim = 0

    d1 = get_duration(video1_path)
    d2 = get_duration(video2_path)
    duration_sim = max(0, 100 - abs(d1 - d2))

    # ---------- EVIDENCE ----------
    evidence_timeline = compute_frame_match_timeline(video1_path, video2_path)
    evidence_frames = get_evidence_frames(video1_path, video2_path)

    # ---------- FINAL SCORE ----------
    final_score = (
        0.30 * frame_similarity +
        0.15 * thumb_similarity +
        0.10 * duration_sim +
        0.20 * clip_sim +
        0.25 * audio_sim
    )

    final_score = round(final_score, 2)

    # ---------- PROPAGATION ----------
    propagation = generate_propagation(final_score)

    risk = "HIGH" if final_score > 75 else "MEDIUM" if final_score > 40 else "LOW"

    return {
        "similarity": final_score,
        "frame_similarity": frame_similarity,
        "thumbnail_similarity": thumb_similarity,
        "clip_similarity": clip_sim,
        "audio_similarity": audio_sim,
        "duration_similarity": duration_sim,

        "clip_label_1": clip_explanation.get("video1_concepts", []),
        "clip_label_2": clip_explanation.get("video2_concepts", []),
        "clip_common": clip_explanation.get("common_concepts", []),

        "evidence_timeline": evidence_timeline,
        "evidence_frames": evidence_frames,

        "propagation": propagation,

        "risk": risk
    }