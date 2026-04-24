import streamlit as st
import tempfile
import time
import json

from step3_safe_fingerprint import run_pipeline
from youtube_collector import search_videos
from report_generator import generate_report

from evaluation_engine import evaluate_model, predict

st.set_page_config(layout="wide", page_title="Authentiplay AI")

# ================= UI STYLE =================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0b0f1a, #000);
    color: white;
}

.title {
    font-size: 48px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg,#00f5ff,#ff00c8,#7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.section {
    font-size: 22px;
    margin-top: 20px;
    color: #00f5ff;
    font-weight: 700;
}

.card {
    background: rgba(255,255,255,0.06);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown('<div class="title">🎬 AUTHENTIPLAY AI</div>', unsafe_allow_html=True)

# ================= SEARCH =================
query = st.text_input("Search Content", "cricket")

videos = []
try:
    videos = search_videos(query)
except:
    st.warning("API issue")

# ================= UPLOAD =================
v1 = st.file_uploader("📤 Original Video", type=["mp4"])
v2 = st.file_uploader("📤 Suspected Video", type=["mp4"])

# ================= MAIN =================
if v1 and v2:

    st.markdown("## 🎥 Video Analysis")

    c1, c2 = st.columns(2)

    with c1:
        st.video(v1)

    with c2:
        st.video(v2)

    if st.button("🚀 RUN AI INVESTIGATION"):

        with tempfile.NamedTemporaryFile(delete=False) as f1:
            f1.write(v1.read())
            p1 = f1.name

        with tempfile.NamedTemporaryFile(delete=False) as f2:
            f2.write(v2.read())
            p2 = f2.name

        with st.spinner("🧠 Running Multi-Modal AI..."):
            result = run_pipeline(p1, p2)

        # ================= RESULT =================
        st.success(f"Final Similarity: {result['similarity']}%")
        st.info(f"Risk Level: {result['risk']}")

        # ================= METRICS =================
        st.markdown("## 🧠 Multi-Modal Breakdown")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Frame", f"{result['frame_similarity']}%")
        c2.metric("Thumbnail", f"{result['thumbnail_similarity']}%")
        c3.metric("CLIP", f"{result['clip_similarity']}%")
        c4.metric("Audio", f"{result['audio_similarity']}%")

        # ================= CLIP =================
        st.markdown("## 🧠 AI Reasoning")

        st.write("Video 1:", result.get("clip_label_1", []))
        st.write("Video 2:", result.get("clip_label_2", []))
        st.success(result.get("clip_common", []))

        # ================= EVIDENCE =================
        st.markdown("## 🔬 Evidence Panel")

        timeline = result.get("evidence_timeline", [])

        if timeline:
            st.line_chart([t["similarity"] for t in timeline])

        frames = result.get("evidence_frames", [])

        st.markdown("### 🧪 Matching Frames")

        if frames:
            for f in frames[:5]:
                st.write(f"Frame {f['frame_index']} → {f['score']:.2f}%")
        else:
            st.write("No strong matches found")

        # ================= PROPAGATION =================
        st.markdown("## 🌍 Propagation Model")

        prop = result.get("propagation", {})

        st.write("Origin:", prop.get("origin"))
        st.write("Nodes:", prop.get("nodes"))

        for e in prop.get("edges", []):
            st.write(f"{e['from']} ➜ {e['to']} | {e['probability']}")

        # ================= REPORT =================
        st.markdown("## 📄 AI Report")

        if st.button("📥 Generate PDF Report"):
            file = generate_report(result)

            with open(file, "rb") as f:
                st.download_button(
                    "⬇ Download Report",
                    f,
                    file_name="Authentiplay_Report.pdf",
                    mime="application/pdf"
                )

# ================= EVALUATION =================
st.markdown("## 📊 Model Evaluation Dashboard")

if st.button("📈 Run Evaluation"):

    try:
        data = json.load(open("dataset.json"))

        preds = []
        labels = []

        for d in data:
            r = run_pipeline(d["video_a"], d["video_b"])

            preds.append(predict(r["similarity"]))
            labels.append(d["label"])

        metrics = evaluate_model(preds, labels)

        st.success("Evaluation Completed")

        st.json(metrics)

    except Exception as e:
        st.error(f"Evaluation Error: {e}")